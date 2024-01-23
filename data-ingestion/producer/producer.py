from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from pulsar import Client

PULSAR_HOST = "pulsar://localhost:6650"

if __name__ == "__main__":
    loader = WebBaseLoader(
        [
            "https://engineering.fb.com/2024/01/18/developer-tools/lazy-imports-cinder-machine-learning-meta/",
            "https://peps.python.org/pep-0690/",
            "https://developers.facebook.com/blog/post/2022/06/15/python-lazy-imports-with-cinder/"
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
