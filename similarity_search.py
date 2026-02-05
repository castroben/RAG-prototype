from azure.cosmos import CosmosClient, PartitionKey, exceptions
from db_conn import get_cosmos_container_conn
from embed import embed
import urllib3
import json

# Disable warning for missing SSL certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Follow Azure CosmosDB emulator documentation
# https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-develop-emulator
# Start local instance with cosmos-startup.sh
URL = "https://localhost:8081"
KEY = "C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=="
DATABASE_NAME = "FootballNewsDB"
CONTAINER_NAME = "25-26"

client = CosmosClient(URL, credential=KEY)

def save_item(container, id, content, vector, metadata):
    item = {
        "id": id,
        "content": content,
        "contentVector": vector
    }
    item.update(metadata)

    container.upsert_item(item)
    print(f"saved item={id} successfully")


def similarity_search(container, query_vector, limit=2):
    # The 'VectorDistance' function is the magic that finds similar records
    query = f"""
    SELECT TOP {limit} c.title, c.content, VectorDistance(c.contentVector, @embedding) AS SimilarityScore
    FROM c
    ORDER BY VectorDistance(c.contentVector, @embedding)
    """

    results = container.query_items(
        query=query,
        parameters=[{"name": "@embedding", "value": query_vector}],
        enable_cross_partition_query=True
    )

    return list(results)

container = get_cosmos_container_conn()

# container_properties = container.read()
# print(json.dumps(container_properties, indent=2))


content = "Madrid Update\nMbappe scores a hat-trick in the 2025 opener..."
vector = embed(content, mode="DOC")
save_item(
    container,
    "00000000-0000-0000-0000-000000000000",
    content,
    vector,
    {
        "title": "Madrid Update"
    }
)

user_query = "Who scored in  the 2025 opener?"
user_query_vector = embed(user_query, "QUERY")

similarity_search(container, user_query_vector)
matches = similarity_search(container, user_query_vector)

print("top matches for query:")
for match in matches:
    print(f"{match['title']} (Score: {match['SimilarityScore']:.4f})")