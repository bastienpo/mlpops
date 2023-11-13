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
milvus_collection_name = "embedding_collection"
milvus_port = '19530'
milvus_host = 'localhost'
milvus_threshold_similarity = 0.9

connections.connect("default", host="localhost", port="19530")

# Create collection -- TODO update fields to match embeddings
fields = [
    FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=512),
    FieldSchema(name="prediction", dtype=DataType.VARCHAR, max_length=10000),
]
schema = CollectionSchema(fields, f"{milvus_collection_name} is the name of the embedding collection")
embedding_collection = Collection(milvus_collection_name, schema)

# Create index for milvus data - Organize data for faster search
index = {
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "params": {"nlist": 4},
}
embedding_collection.create_index(field_name="embeddings", index_params=index)

"""
Embedding setup
"""
embedding_model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-small-en', trust_remote_code=True) # trust_remote_code is needed to use the encode method

"""
Temporary LLM setup (to be replaced by a container)
"""
# model = AutoModel.from_pretrained("TheBloke/Mistral-7B-v0.1-GGUF", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("TheBloke/Mistral-7B-v0.1-GGUF", model_file="mistral-7b-v0.1.Q4_K_M.gguf", model_type="mistral", gpu_layers=0) # No GPU

"""
Main logic
"""
# TODO: add FASTAPI endpoint to send and recieve messages from frontend

def search_embedding(embedding):
    """
    Search embedding in database
    :param embedding: embedding to search (numpy array)
    """
    embedding_collection.load() # Put our collection in memory

    search = embedding_collection.search([embedding], anns_field="embeddings", param={"nprobe": 16}, limit=1, output_fields=["prediction"])
    
    embedding_collection.release() # Remove our collection from memory

    return search[0] # Only one item searched

def predict_and_insert(msg, embedding):
    print("Computing result")
    prediction = model(msg) # TODO: replace with api call to LLM container
    
    # Store result in database
    embedding_collection.insert({"embeddings": embedding, "prediction": prediction}) # Automatically add pk

    return prediction


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
    print(f"Processing: {msg}")

    embedding = embedding_model.encode(msg)

    # Search embedding in database
    best_hit = search_embedding(embedding)

    # Check if best hit in db is similar enough
    if len(best_hit) and best_hit[0].distance <= milvus_threshold_similarity:
        
        # Return stored result
        print("Found similar embedding in database")
        return best_hit[0].entity.get("prediction")

    # Compute result and store it in database
    return predict_and_insert(msg, embedding)

process_message("What is the universal answer ?")
process_message("What is the universal answer ?")

client.close()