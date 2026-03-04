import whisper
import torch
import os

print("Loading Whisper model (medium)...")

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

model = whisper.load_model("medium").to(DEVICE)

print(f"Whisper model loaded on {DEVICE}")


def transcribe_audio(audio_path: str):

    if not os.path.exists(audio_path):
        print("Audio file not found:", audio_path)
        return ""

    try:
        result = model.transcribe(
            audio_path,
            fp16=torch.cuda.is_available(),
            language="en"
        )

        text = result.get("text", "").strip()

        return text

    except Exception as e:
        print("Transcription error:", e)
        return ""