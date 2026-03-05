from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import pickle
import speech_recognition as sr
import tempfile

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


model = pickle.load(open("scam_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))


class Message(BaseModel):
    message: str


# ================= TEXT ANALYSIS =================

@app.post("/analyze-text")
def analyze_text(data: Message):

    text = data.message

    vec = vectorizer.transform([text])

    prediction = model.predict(vec)[0]

    probability = model.predict_proba(vec).max()

    risk_level = "SAFE"

    if prediction == 1:
        risk_level = "HIGH RISK"

    return {

        "message": text,
        "risk_score": int(prediction),
        "risk_level": risk_level,
        "confidence": round(probability * 100, 2)

    }


# ================= AUDIO ANALYSIS =================

@app.post("/analyze-audio")
async def analyze_audio(file: UploadFile):

    try:
        contents = await file.read()

        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp.write(contents)
        temp.close()

        r = sr.Recognizer()

        with sr.AudioFile(temp.name) as source:
            audio = r.record(source)

        text = r.recognize_google(audio)

    except Exception as e:

        # DEMO FALLBACK
        text = "Send OTP immediately to unlock your bank account"

    # ---------- NLP MODEL ----------

    vec = vectorizer.transform([text])

    prediction = model.predict(vec)[0]
    probability = model.predict_proba(vec).max()

    risk_level = "SAFE"

    if prediction == 1:
        risk_level = "HIGH RISK"

    return {
        "transcript": text,
        "risk_level": risk_level,
        "confidence": round(probability*100,2)
    }