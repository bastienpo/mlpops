"""
Langchain chain for RAG model with Milvus
"""

from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

HUGGINGFACEHUB_API_TOKEN = "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"

API_URL = (
    "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0"
)


template = """ {question} """

prompt = ChatPromptTemplate.from_template(template)

model = HuggingFaceEndpoint(
    endpoint_url=API_URL,
    task="text-generation",
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
)

chain = prompt | model | StrOutputParser()
