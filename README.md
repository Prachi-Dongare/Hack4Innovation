
# Scam Shield – AI Based Scam Detection Extension

Scam Shield is a browser extension that detects potential scam messages using Natural Language Processing (NLP) and Machine Learning.  
It analyzes text, voice input, and audio files to identify common fraud patterns such as OTP scams and phishing messages.

## Features
- Text scam detection
- Voice-to-text scam analysis
- Audio file scam detection
- Machine learning based classification
- Simple browser extension interface

## Tech Stack
- Python
- FastAPI
- Scikit-learn
- SpeechRecognition
- JavaScript (Chrome Extension)

## How It Works

Input (Text / Voice / Audio)  
↓  
Speech-to-Text Conversion  
↓  
NLP Vectorization  
↓  
ML Scam Detection Model  
↓  
Risk Classification (SAFE / HIGH RISK)

## Run Backend

pip install fastapi uvicorn scikit-learn speechrecognition python-multipart  
uvicorn app.api.server:app --reload

## Example

Input:  
Send OTP immediately to unlock your bank account  

Output:  
Risk Level: HIGH RISK  
Confidence: 75%

---

Built as part of a Cyber Safety project to help detect online scams using AI.
