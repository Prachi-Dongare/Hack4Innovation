import os
import pandas as pd
import torch

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments
)

DATA_PATH = "data/processed/scam_dataset.csv"
MODEL_DIR = "app/nlp_model/model"

df = pd.read_csv(DATA_PATH)

texts = df["text"].tolist()
labels = df["label"].tolist()

label_encoder = LabelEncoder()
labels_encoded = label_encoder.fit_transform(labels)

train_texts, val_texts, train_labels, val_labels = train_test_split(
    texts,
    labels_encoded,
    test_size=0.1
)

tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

train_encodings = tokenizer(train_texts, truncation=True, padding=True)
val_encodings = tokenizer(val_texts, truncation=True, padding=True)


class ScamDataset(torch.utils.data.Dataset):

    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):

        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])

        return item

    def __len__(self):
        return len(self.labels)


train_dataset = ScamDataset(train_encodings, train_labels)
val_dataset = ScamDataset(val_encodings, val_labels)

model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=len(label_encoder.classes_)
)

training_args = TrainingArguments(
    output_dir=MODEL_DIR,
    learning_rate=5e-5,
    per_device_train_batch_size=16,
    num_train_epochs=3,
    save_strategy="epoch"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

trainer.train()

os.makedirs(MODEL_DIR, exist_ok=True)

model.save_pretrained(MODEL_DIR)
tokenizer.save_pretrained(MODEL_DIR)

torch.save(label_encoder, os.path.join(MODEL_DIR, "label_encoder.pt"))

print("Training complete")