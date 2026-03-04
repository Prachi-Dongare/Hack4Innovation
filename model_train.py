import pandas as pd
import re
import string
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score


# =========================================================
# LABEL MAP
# =========================================================

label_names = {
    0: "Safe Message",
    1: "Phishing / Spam",
    2: "Digital Arrest",
    3: "Job Scam",
    4: "Investment Scam"
}


# =========================================================
# LOAD DATASETS
# =========================================================

print("Loading datasets...")

# SMS Spam dataset
sms_df = pd.read_csv("spam.csv", encoding="latin-1")
sms_df = sms_df[['v1','v2']]
sms_df.columns = ['label','text']

sms_df['label'] = sms_df['label'].map({
    'ham':0,
    'spam':1
})


# Phishing emails
email_df = pd.read_csv("phishing_email.csv")
email_df = email_df[['text_combined']]
email_df.columns = ['text']
email_df['label'] = 1


# Digital arrest scams
digital_df = pd.read_csv("digital_arrest.csv")


# Job scam dataset
job_df = pd.read_csv("job_scam.csv")


# Investment scam dataset
invest_df = pd.read_csv("investment_scam.csv")


# =========================================================
# COMBINE DATA
# =========================================================

combined_df = pd.concat([
    sms_df,
    email_df,
    digital_df,
    job_df,
    invest_df
], ignore_index=True)

print("Total messages:", len(combined_df))


# =========================================================
# TEXT CLEANING
# =========================================================

def clean_text(text):

    text = str(text).lower()

    text = re.sub(r'\d+', '', text)

    text = text.translate(str.maketrans('', '', string.punctuation))

    text = text.strip()

    return text


combined_df['text'] = combined_df['text'].apply(clean_text)


# =========================================================
# TF-IDF VECTORIZATION
# =========================================================

vectorizer = TfidfVectorizer(
    max_features=20000,
    ngram_range=(1,3),
    stop_words="english"
)

X = vectorizer.fit_transform(combined_df['text'])

y = combined_df['label']


# =========================================================
# TRAIN TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# =========================================================
# MODEL TRAINING
# =========================================================

print("\nTraining model...")

model = LogisticRegression(
    max_iter=2000,
    multi_class="multinomial"
)

model.fit(X_train, y_train)


# =========================================================
# EVALUATION
# =========================================================

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", accuracy)

print("\nClassification Report:\n")

print(classification_report(y_test, y_pred))


# =========================================================
# SAVE MODEL
# =========================================================

pickle.dump(model, open("scam_model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("\nModel saved successfully.")


# =========================================================
# SCAM EXPLANATION PATTERNS
# =========================================================

scam_patterns = {

    "authority threat": [
        "police",
        "investigation",
        "court",
        "arrest",
        "legal action",
        "cyber crime"
    ],

    "urgency language": [
        "urgent",
        "immediately",
        "act now",
        "within 24 hours"
    ],

    "financial request": [
        "transfer money",
        "send payment",
        "deposit funds"
    ],

    "phishing attempt": [
        "click the link",
        "verify your account",
        "login to your account",
        "confirm your identity"
    ]
}


# =========================================================
# EXPLANATION ENGINE
# =========================================================

def explain_message(message):

    message = message.lower()

    reasons = []

    for category, phrases in scam_patterns.items():

        for phrase in phrases:

            if phrase in message:

                reasons.append(category)

    return list(set(reasons))


# =========================================================
# HIGHLIGHT WORDS
# =========================================================

def highlight_words(message):

    highlighted = message

    for category, phrases in scam_patterns.items():

        for phrase in phrases:

            highlighted = re.sub(
                phrase,
                f"[{phrase.upper()}]",
                highlighted,
                flags=re.IGNORECASE
            )

    return highlighted


# =========================================================
# URL DETECTION
# =========================================================

def extract_urls(text):

    return re.findall(r'https?://\S+|www\.\S+', text)


# =========================================================
# PREDICTION FUNCTION
# =========================================================

def predict_message(message):

    cleaned = clean_text(message)

    vector = vectorizer.transform([cleaned])

    prediction = model.predict(vector)[0]

    probs = model.predict_proba(vector)[0]

    risk = int(max(probs) * 100)

    scam_type = label_names[prediction]

    if prediction == 0:
        result = "Safe Message"
    else:
        result = "Scam Detected"

    reasons = explain_message(message)

    highlighted = highlight_words(message)

    urls = extract_urls(message)

    return result, scam_type, risk, reasons, highlighted, urls


# =========================================================
# MULTI-LINE INPUT SYSTEM
# =========================================================

while True:

    print("\nPaste your message (type END on new line to analyze):")

    lines = []

    while True:

        line = input()

        if line.strip().upper() == "END":
            break

        lines.append(line)

    message = "\n".join(lines)

    if message.lower() == "exit":
        break

    result, scam_type, risk, reasons, highlighted, urls = predict_message(message)

    print("\nAnalysis Result")
    print("----------------------------")

    print("Result:", result)
    print("Scam Type:", scam_type)
    print("Risk Score:", risk, "%")

    print("\nHighlighted Message:\n")
    print(highlighted)

    if reasons:
        print("\nExplanation:", ", ".join(reasons))
    else:
        print("\nExplanation: No suspicious indicators detected")

    if urls:
        print("\nURLs Detected:")
        for u in urls:
            print("-", u)