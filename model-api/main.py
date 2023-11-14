import os

import requests
from fastapi import FastAPI
from pydantic import BaseModel
import pulsar

# TODO call embedding servcice

app = FastAPI()


class TextItem(BaseModel):
    text: str


pulsar_client = pulsar.Client("pulsar://localhost:6650")


# @app.post("/predict")
# def predict(data: TextItem):
#     response = query(payload={"inputs": data.text})

#     return response[0].get("generated_text")
