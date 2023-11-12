import os

import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
secret_key = os.environ.get("HF_SECRET_KEY")

MODEL_API_URL = (
    "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
)
headers = {"Authorization": secret_key}


class TextItem(BaseModel):
    text: str


def query(payload):
    response = requests.post(MODEL_API_URL, headers=headers, json=payload)
    return response.json()


@app.post("/predict")
def predict(data: TextItem):
    response = query(payload={"inputs": data.text})

    return response[0].get("generated_text")
