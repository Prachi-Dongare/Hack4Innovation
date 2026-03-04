from fastapi import FastAPI
from app.stt.whisper_engine import transcribe_audio
from app.nlp_model.inference import predict_scam

app = FastAPI()


@app.get("/")
def home():
    return {"status": "Scam Detection API running"}


@app.post("/detect")

def detect(audio_path: str):

    text = transcribe_audio(audio_path)

    label, confidence = predict_scam(text)

    return {
        "transcript": text,
        "scam_type": label,
        "confidence": confidence
    }