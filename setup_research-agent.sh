#!/bin/bash

# Create project root
mkdir -p research-agent
cd research-agent

# Create directories
mkdir -p data
mkdir -p data/raw
mkdir -p data/processed

mkdir -p src
mkdir -p src/agents
mkdir -p src/ingest
mkdir -p src/indexer
mkdir -p src/utils

mkdir -p tests

# Create placeholder files
touch src/app.py
touch src/agents/router.py
touch src/agents/web_agent.py
touch src/agents/rag_agent.py
touch src/agents/summarizer.py
touch src/ingest/pdf_loader.py
touch src/indexer/embed_and_index.py
touch requirements.txt
touch README.md

echo "Project structure created."
