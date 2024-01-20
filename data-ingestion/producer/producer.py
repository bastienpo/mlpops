from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from pulsar import Client

PULSAR_HOST = "pulsar://localhost:6650"

if __name__ == "__main__":
    loader = WebBaseLoader(
        [
            "https://fr.wikipedia.org/wiki/Google",
        ]
    )

    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=0)
    splits = splitter.split_documents(docs)

    client = Client(PULSAR_HOST)
    producer = client.create_producer("topic_retrival")

    for split in splits:
        try:
            producer.send(split.page_content.encode("utf-8"), None)
        except Exception as e:
            print(e)

    producer.flush()
    producer.close()
