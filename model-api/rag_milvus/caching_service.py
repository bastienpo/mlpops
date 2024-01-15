import pulsar
from transformers import AutoModel
from ctransformers import AutoModelForCausalLM
from numpy.linalg import norm
from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)

# TODO - variables d'environnement
pulsar_service_url = "pulsar://localhost:6650"
pulsar_topic = "prediction-topic"
pulsar_subscription = "prediction-subscription"

client = pulsar.Client(pulsar_service_url)

consumer = (
    client.newConsumer()
    .topic(pulsar_topic)
    .subscriptionName(pulsar_subscription)
    .subscribe()
)

"""
Milvus setup
"""
# TODO - variables d'environnement
milvus_collection_name = "embedding_collection"
milvus_port = "19530"
milvus_host = "localhost"

connections.connect("default", host="localhost", port="19530")

# Create collection
fields = [
    FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=512),
    FieldSchema(name="prediction", dtype=DataType.VARCHAR, max_length=10000),
]
schema = CollectionSchema(
    fields, f"{milvus_collection_name} is the name of the embedding collection"
)
embedding_collection = Collection(milvus_collection_name, schema)

while True:
    # Consume message
    msg = (
        consumer.receive()
    )  # {"embedding"": [0.1, 0.2, ...], "prediction": "Why is Ai not really AI ? AI don't know."}

    try:
        # Insert message in Milvus
        embedding_collection.insert([msg.value()])

        # Ack message
        consumer.acknowledge(msg)

    except:
        # Message failed to be inserted in Milvus
        consumer.negativeAcknowledge(msg)

client.close()
