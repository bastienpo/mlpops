from pulsar import Client
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Milvus

PULSAR_HOST = "pulsar://localhost:6650"
MILVUS_HOST = "localhost"
MILVUS_PORT = 19530

if __name__ == "__main__":
    client = Client(PULSAR_HOST)
    consumer = client.subscribe("topic_retrival", "sub_retrival")

    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

    milvus_store = Milvus(
        embedding_function = embeddings,
        connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT},
    )

    while True:
        msg = consumer.receive()
        try:
            decoded_str = msg.data().decode('utf-8')

            milvus_store.add_texts(
                [decoded_str]
            )
            
            print(f"Added text to Milvus: {msg.message_id()}")

            # Acknowledge successful processing of message
            consumer.acknowledge(msg)
        except Exception:
            consumer.negative_acknowledge(msg)
        
    client.close()

