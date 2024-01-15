"""
Langchain chain for RAG model with Milvus
"""

from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from .prompt import llama_prompt_template
from .retriever import vector_db

HUGGINGFACEHUB_API_TOKEN = "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"

API_URL = (
    "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0"
)


prompt = ChatPromptTemplate.from_template(llama_prompt_template)

retriever = vector_db.as_retriever()

model = HuggingFaceEndpoint(
    endpoint_url=API_URL,
    task="text-generation",
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
)

chain = (
    RunnableParallel({"context": retriever, "message": RunnablePassthrough()})
    | prompt
    | model
    | StrOutputParser()
)
