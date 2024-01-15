"""

"""

from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores.milvus import Milvus

MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"

# Load documents from the web
loader = WebBaseLoader(
    [
        "https://www.wikihow.com/Be-a-Good-Student",
    ]
)

docs = loader.load()

# Split documents into chunks of 1024 characters
text_splitter = CharacterTextSplitter(chunk_size=1024, chunk_overlap=0)
docs = text_splitter.split_documents(docs)

embeddings_model = HuggingFaceInferenceAPIEmbeddings(
    api_key="", model_name="sentence-transformers/paraphrase-xlm-r-multilingual-v1"
)

vector_store = Milvus.from_documents(
    docs,
    embedding=embeddings_model,
    connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT},
)
