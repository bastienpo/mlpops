from langchain_community.document_loaders import WebBaseLoader
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.vectorstores.milvus import Milvus
from langchain.text_splitter import SentenceTransformersTokenTextSplitter
from pulsar import Client

# MILVUS_HOST = "host.docker.internal"
# MILVUS_PORT = "19530"
PULSAR_HOST = "pulsar://host.docker.internal:6650"

loader = WebBaseLoader(
    [
        "https://fr.wikipedia.org/wiki/Google",
    ]
)

docs = loader.load()
splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=0, tokens_per_chunk=256)
splits = splitter.split_documents(docs)

client = Client(PULSAR_HOST)
producer = client.create_producer(
    "collection_retrival", 
    batching_enabled=True,
    block_if_queue_full=True,
    properties={
        "producer_name": "producer_retrival_name",
        "producer_id": "producer_retrival_id",
    }
)

for split in splits:
    try:
        producer.send(split.page_content.encode("utf-8"), None)
    except Exception as e:
        print(e)

producer.flush()
producer.close()

# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# vector_db = Milvus.from_documents(
#     documents=splits,
#     embedding=embeddings,
#     connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT},
#     collection_name="collection_retrival",
# )
