"""
RAG with Milvus and distilbert-base-uncased Embeddings
"""

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Milvus

MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"

model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": False}

embeddings = HuggingFaceEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)

vector_db = Milvus(
    embedding_function=embeddings,
    connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT},
)
