# RAG-prototype
Very much WIP

High level:
1. Ingestion engine: exctract web content, convert to markdown
2. Data processing: embed markdown, save to vector DB
3. Semantic search: embed user query, search against vector DB
4. RAG: feed semantic search contextual data to LLM

### Running Cosmos DB Emulator on Docker
https://github.com/Azure/azure-cosmos-db-emulator-docker
```
docker run --detach `
  --publish 8081:8081 --publish 1234:1234 `
  --name cosmos-emulator`
  mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:vnext-preview `
  --protocol https
```
`vnext-preview` is configured to work with WSL2, which fixes networking issues when docker containers through WSL2.
`localhost:8081` for DB client connection.
`localhost:1234` for DB explorer UI.

Next Steps:
- chunking strategy for markdown documents
- generate chunks embeddings using LLM
