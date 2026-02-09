from azure.cosmos import CosmosClient
from data.db_conn import get_cosmos_container_conn
from model.embed import embed
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

def similarity_search(container, query_vector, limit=2):
    # The 'VectorDistance' function is the magic that finds similar records
    query = f"""
    SELECT TOP {limit} c.id, c.content, VectorDistance(c.contentVector, @embedding) AS SimilarityScore
    FROM c
    ORDER BY VectorDistance(c.contentVector, @embedding)
    """

    results = container.query_items(
        query=query,
        parameters=[{"name": "@embedding", "value": query_vector}],
        enable_cross_partition_query=True
    )

    return list(results)