import os
import time
import queue
import threading
import sounddevice as sd
import soundfile as sf

from app.stt.whisper_engine import transcribe_audio
from app.nlp_model.inference import predict_scam
from app.risk_engine.risk_analyzer import update_risk
from app.audio.vad_engine import is_silent
from app.tone_analysis.tone_detector import detect_indicators


SAMPLE_RATE = 16000
CHUNK_DURATION = 3

audio_queue = queue.Queue()

stop_event = threading.Event()

os.makedirs("temp_chunks", exist_ok=True)


def record_audio():

    chunk_id = 0

    while not stop_event.is_set():

        chunk_id += 1

        print(f"\n🎙 Recording chunk {chunk_id}...")

        audio = sd.rec(
            int(SAMPLE_RATE * CHUNK_DURATION),
            samplerate=SAMPLE_RATE,
            channels=1
        )

        sd.wait()

        if stop_event.is_set():
            break

        if is_silent(audio):

            print("🔇 Skipping silent chunk")
            continue

        file_path = f"temp_chunks/chunk_{chunk_id}.wav"

        sf.write(file_path, audio, SAMPLE_RATE)

        print("Saved:", file_path)

        audio_queue.put(file_path)


def process_audio():

    context = ""

    while not stop_event.is_set():

        try:

            audio_file = audio_queue.get(timeout=0.5)

        except queue.Empty:
            continue

        start_time = time.time()

        text = transcribe_audio(audio_file)

        if not text:
            continue

        context = (context + " " + text).strip()

        if len(context) > 300:
            context = context[-300:]

        label, confidence = predict_scam(context)

        risk_level, history, critical = update_risk(label, confidence)

        indicators = detect_indicators(text)

        print("\n📝 Transcript:", text)
        print("🧠 Context Used:", context)

        print("🚨 Scam Type:", label)
        print(f"📊 Confidence: {confidence*100:.2f}%")
        print("⚠ Risk Level:", risk_level)

        if indicators:

            print("\n🔎 Indicators Detected")

            for word in indicators:
                print("•", word)

        if critical:
            print("\n🔴 CRITICAL ALERT: Repeated scam indicators detected!")

        print("\n📈 Risk Timeline")

        for i, r in enumerate(history):
            print(f"[{i+1}] {r}")

        end_time = time.time()

        print(f"\n⏱ Processing time: {end_time-start_time:.2f} sec")

        audio_queue.task_done()


def start_streaming():

    print("\n🚀 Real-Time Scam Detection Started")
    print("Press Ctrl+C to stop\n")

    recorder = threading.Thread(target=record_audio, daemon=True)
    processor = threading.Thread(target=process_audio, daemon=True)

    recorder.start()
    processor.start()

    try:

        while True:
            time.sleep(0.5)

    except KeyboardInterrupt:

        print("\n\n🛑 Stopping system...")

        stop_event.set()

        sd.stop()

        print("✅ System stopped safely")


if __name__ == "__main__":
    start_streaming()