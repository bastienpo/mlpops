"""
RAG with Milvus and distilbert-base-uncased Embeddings
"""

from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores.milvus import Milvus

HUGGINGFACEHUB_API_TOKEN = "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"
MILVUS_HOST = "host.docker.internal"
MILVUS_PORT = "19530"

embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=HUGGINGFACEHUB_API_TOKEN,
    model_name="distilbert-base-uncased",
)

vector_db = Milvus(
    embeddings,
    connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT},
    collection_name="collection_retrival",
)
