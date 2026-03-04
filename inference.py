import os
import torch
from transformers import DistilBertTokenizerFast
from transformers import DistilBertForSequenceClassification
from sklearn.preprocessing import LabelEncoder

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model")

print("Loading fine-tuned DistilBERT model...")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_PATH)

model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)

model.to(device)

model.eval()

label_encoder = torch.load(
    os.path.join(MODEL_PATH, "label_encoder.pt"),
    weights_only=False
)

print(f"Model loaded on {device}")


def predict_scam(text):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=256
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():

        outputs = model(**inputs)

        probs = torch.softmax(outputs.logits, dim=1)

        confidence, predicted = torch.max(probs, dim=1)

    label = label_encoder.inverse_transform([predicted.cpu().item()])[0]

    return label, confidence.cpu().item()