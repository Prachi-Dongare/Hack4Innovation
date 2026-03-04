import pandas as pd
import random

scam_en = [
    "please share your otp",
    "your bank account has been blocked",
    "this is bank verification department",
    "verify your account immediately",
    "share your otp now",
    "confirm debit card details",
    "your account will be suspended",
]

scam_hi = [
    "kripya apna otp bataye",
    "aapka bank account block ho gaya hai",
    "ye bank verification department se bol rahe hain",
    "turant apna otp share kijiye",
    "account verify karna zaroori hai",
]

normal_en = [
    "hello how are you",
    "good morning",
    "what are you doing",
    "let us meet tomorrow",
    "did you complete assignment",
    "please send the report",
    "how is your day going",
]

normal_hi = [
    "namaste aap kaise ho",
    "kal milte hain",
    "assignment complete hua kya",
    "report bhej dena",
    "aaj ka din acha hai",
]

data = []

for _ in range(9000):
    data.append([random.choice(scam_en), "OTP_Bank_Fraud"])

for _ in range(6000):
    data.append([random.choice(scam_hi), "OTP_Bank_Fraud"])

for _ in range(7000):
    data.append([random.choice(normal_en), "Normal_Conversation"])

for _ in range(3000):
    data.append([random.choice(normal_hi), "Normal_Conversation"])

random.shuffle(data)

df = pd.DataFrame(data, columns=["text","label"])

df.to_csv("data/processed/scam_dataset.csv", index=False)

print("Dataset generated:", len(df))