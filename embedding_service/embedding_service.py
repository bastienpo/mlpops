import pulsar
from transformers import AutoModel
from numpy.linalg import norm
from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)


"""
Pulsar setup
"""
# TODO - variables d'environnement
pulsar_service_url = 'pulsar://localhost:6650'
pulsar_topic = 'my-topic'
pulsar_subscription = 'my-subscription'

client = pulsar.Client(pulsar_service_url)

"""
Milvus setup
"""
# TODO - variables d'environnement
milvus_collection_name = 'my-collection'
milvus_port = '19530'
milvus_host = 'localhost'
milvus_threshold_similarity = 0.9

connections.connect("default", host="localhost", port="19530")

# Create collection -- TODO update fields to match embeddings
collection_name = "embedding_collection"
fields = [
    FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=8192),
    FieldSchema(name="prediction", dtype=DataType.VARCHAR, max_length=10000),
]
schema = CollectionSchema(fields, f"{collection_name} is the name of the embedding collection")
embedding_collection = Collection(collection_name, schema)

# Create index for milvus data - Organize data for faster search
index = {
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "params": {"nlist": 4},
}

"""
Embedding setup
"""
embedding_model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-small-en', trust_remote_code=True) # trust_remote_code is needed to use the encode method

"""
Main logic
"""
# TODO: add FASTAPI endpoint to send and recieve messages from frontend

def process_message(msg):
    """
    - Compute embedding
    - Check if embedding is in database
        - Yes:
            - Return stored result
        - No:
            - Compute result
            - Store result in database
            - Return result
    :param msg: input to process (string)
    """
    print(f"Processing message: {msg}")

    embedding = embedding_model.encode(msg)[0]

    # Search embedding in database
    search = embedding_collection.search(embedding, anns_field="embeddings", param={"nprobe": 16}, limit=1)
    best_hit = search[0][0] # Only one item searched and only one result asked

    # Check if best hit is similar enough
    if len(best_hit) and best_hit["distance"] > milvus_threshold_similarity:
        # Return stored result
        print("Found similar embedding in database")
        return best_hit["entity"].get("prediction")

    # Compute result
    print("Computing result")
    prediction = "This is a prediction" # TODO add prediction logic

    # Store result in database
    embedding_collection.insert([[embedding, prediction]]) # Automatically add pk

    # Return result
    return prediction

client.close()