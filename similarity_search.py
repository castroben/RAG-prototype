from azure.cosmos import CosmosClient, PartitionKey, exceptions
from db_conn import get_cosmos_container_conn
import urllib3

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


def save_document(container, doc_id, title, content, vector):
    # This simulates saving a Markdown-converted news article
    item = {
        "id": doc_id,
        "title": title,
        "content": content,  # Your Markdown content goes here
        "season": "2025/2026",
        "league": "Premier League",
        "contentVector": vector  # The numerical representation of the content
    }
    container.upsert_item(item)
    print(f"saved document={doc_id} successfully")


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

# Mock data
save_document(
    container,
    "1",
    "Mbappe's Dominance in La Liga",
    "### Madrid Update\nMbappe scores a hat-trick in the 2025 opener...",
    [0.1, 0.9, 0.5] # Replace with model embeddings
)

# Simulate query"
user_query_vector = [0.12, 0.88, 0.45]
matches = similarity_search(container, user_query_vector)

print("top matches for query:")
for match in matches:
    print(f"{match['title']} (Score: {match['SimilarityScore']:.4f})")