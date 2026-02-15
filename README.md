# RAG-prototype
Very much WIP

High level:
1. Ingestion: extract web content, embed, save to vector DB
2. Semantic search: embed user query, search against vector DB
3. RAG: feed semantic search contextual data to LLM

### Running Cosmos DB Emulator on Docker
https://github.com/Azure/azure-cosmos-db-emulator-docker
```
docker run --detach `
  --publish 8081:8081 --publish 1234:1234 `
  --name cosmos-emulator`
  mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:vnext-preview `
  --protocol https
```
`vnext-preview` is configured to work with WSL2, which fixes networking issues when docker containers with WSL2.
`localhost:8081` for DB client connection.
`localhost:1234` for DB explorer UI.

### Running OLlama on Windows Machine
https://docs.ollama.com/windows
OLlama starts windows startup, default binding port is `11434`
Python library documentation: https://github.com/ollama/ollama-python

#### Embedding
Using `nomic-embed-text` as embedding model for prototyping

#### Conversation
Using `qwen2.3:3b` for efficiency

### OLlama & Langchain
https://docs.langchain.com/oss/python/integrations/providers/ollama