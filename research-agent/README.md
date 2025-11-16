```
# Research and Summarization Agent (LangGraph)

## Overview
This project implements a research and summarization agent using LangGraph.  
The system routes user queries to one of three paths:
1. LLM reasoning (local Ollama model)
2. Web research (scraping/search)
3. Retrieval-Augmented Generation (RAG) using a local vector database

A final summarization agent synthesizes the gathered information into a structured response.

## Folder Structure
```

```yaml
research-agent/
  data/
    raw/            # original PDFs, datasets
    processed/      # cleaned text chunks
  src/
    agents/
      router.py         # decides LLM / Web / RAG
      web_agent.py      # performs web search + extraction
      rag_agent.py      # handles vector search
      summarizer.py     # final structured answer
    ingest/
      pdf_loader.py     # loads and extracts text from PDFs
    indexer/
      embed_and_index.py # embeddings + vector DB
    utils/              # helper functions
    app.py              # entry point for running the agent
  tests/
  requirements.txt
  README.md
```

```
## Technology Used
- Python
- LangGraph for agent orchestration
- Ollama for local LLM inference
- Chroma / FAISS for vector storage
- SentenceTransformers for embeddings
- Requests + BeautifulSoup4 for web extraction

## Setup Instructions
1. Clone or create the project folder.
2. Run `setup_project.sh` to create the folder structure.
3. Create a virtual environment.
4. Install dependencies from `requirements.txt`.
5. Download or place your dataset/PDFs into `data/raw`.
6. Run the ingestion and indexing scripts.
7. Run `app.py` to submit queries.

## How to Use
- Ingest PDF/dataset → chunk → embed → store in vector DB.
- Start the agent.
- Enter a query.
- Router decides the correct path.
- Summarizer returns a structured final answer.

## Next Steps
- Implement router logic.
- Implement each agent independently.
- Connect nodes using LangGraph.
- Add evaluation tests and example queries.
```

---

# 4. **Steps to set up the project environment**

### Step 1: Make project directory and run setup script

```bash
chmod +x setup_project.sh
./setup_project.sh
```

### Step 2: Create virtual environment

Use Python’s built-in venv:

```bash
python -m venv venv
```

### Step 3: Activate environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### Step 4: Install all dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Verify Ollama is working

```bash
ollama run llama3.2:3b
```

### Step 6: Add your dataset/PDFs to:

```
data/raw/
```

### Step 7: Run the indexing script

(You will write logic later)

```bash
python src/indexer/embed_and_index.py
```

### Step 8: Start the agent

(Once implemented)

```bash
python src/app.py
```

---