from langchain_community.vectorstores import Milvus

from .retriever import embeddings

MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"

query_store = Milvus(
    embedding_function=embeddings,
    collection_name="QueryCollection",
    connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT},
    drop_old=True,
)