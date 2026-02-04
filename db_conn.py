from azure.cosmos import CosmosClient, PartitionKey, exceptions

# Follow Azure CosmosDB emulator documentation
# https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-develop-emulator
# Start local instance with cosmos-startup.sh
URL = "https://localhost:8081"
KEY = "C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=="
DATABASE_NAME = "FootballNewsDB"
CONTAINER_NAME = "25-26"

def get_cosmos_container_conn():
    # Sample vector embedding policy - review: must enable semantic search
    vector_embedding_policy = {
        "vectorEmbeddings": [
            {
                "path": "/contentVector",
                "dataType": "float32",
                "distanceFunction": "cosine",
                "dimensions": 768  # Sample policy - review: must match embeddings dimensions
            }
        ]
    }

    # Sample indexing policy - review: must enable semantic search
    indexing_policy = {
        "indexingMode": "consistent",
        "automatic": True,
        "includedPaths": [
            {"path": "/*"}
        ],
        "excludedPaths": [
            {"path": "/contentVector/*"}
        ],
        "vectorIndexes": [
            {"path": "/contentVector", "type": "flat"}
        ]
    }

    try:
        client = CosmosClient(URL, credential=KEY)
        db = client.create_database_if_not_exists(id=DATABASE_NAME)
        container = db.create_container_if_not_exists(
            id=CONTAINER_NAME,
            partition_key=PartitionKey(path="/id"),
            vector_embedding_policy=vector_embedding_policy,
            indexing_policy=indexing_policy
        )
        print(f"container={CONTAINER_NAME} database={DATABASE_NAME} created successfully")
        return container
    except Exception as e:
        print(f"error creating container={CONTAINER_NAME} database={DATABASE_NAME} error={e}")