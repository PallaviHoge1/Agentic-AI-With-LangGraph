# LangGraph Math Agent (Local Ollama Version)

## Overview
This project implements a simple LangGraph-style agent that can route user queries into two categories:

1. Mathematical queries  
   These are detected using a lightweight regex-based parser and executed locally through predefined math tool functions such as addition, subtraction, multiplication, and division.

2. General questions  
   These are forwarded to a locally running LLM through Ollama (for example `llama3.2:3b`).  
   No paid API key is required for this project.

The goal is to demonstrate tool integration, routing logic, and agent-style workflow similar to LangGraph’s functional structure while running completely offline.

---

## Features
- Detect mathematical expressions such as:
  - `10 - 4`
  - `50 minus 20`
  - `multiply 4 and 6`
  - `divide 12 by 3`
- Compute math locally via Python functions.
- Route non-math queries to local LLM.
- Robust fallback handling and clean error messages.
- Works entirely offline with CPU-only laptops using Ollama.

---

## Project Structure

```yaml
langgraph-math-agent:
  src:
    agent:
      - graph.py
      - __init__.py
    tools:
      - math_tools.py
      - __init__.py
    utils:
      - router.py
      - llm_client.py
      - __init__.py
    - __init__.py
  tests:
    - test_tools.py
  notebooks: []
  README.md: ""
  requirements.txt: ""
```
---

## Folder Structure Notes

* **src/agent/**
  Contains the main logic for query routing and running the agent.

* **src/tools/**
  Contains all predefined mathematical tool functions such as `plus`, `subtract`, `multiply`, `divide`.

* **src/utils/**
  Utility helpers including the math-expression router and Ollama client wrapper.

* **tests/**
  Pytest-based testing for math tools and other components.

* **notebooks/**
  Optional workspace for experimenting, debugging, or prototyping.

---

## Technologies Used

### Python

Main programming language used for the implementation.

### LangGraph Concepts

Although not implementing a full LangGraph graph, the code resembles a LangGraph-style agent architecture:

* Router node
* Tool node
* LLM node
* Output node

### Ollama

Used as a local LLM runtime. The agent forwards general queries to:

```
ollama run <model> --prompt "..."
```

### Regex-based Router

Used to detect whether the query is a mathematical expression or a general natural language question.

---

## Installation and Setup

### 1. Create and activate a virtual environment

```
python -m venv .venv
.venv\Scripts\activate   (Windows)
source .venv/bin/activate (Linux/Mac)
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Install and configure Ollama

Download Ollama from the official website.
Then pull the required model:

```
ollama pull llama3.2:3b
```

### 4. Test Ollama

```
ollama run llama3.2:3b --prompt "Hello"
```

If you see a response, Ollama is working.

---

## Running the Agent

Always run from the project root:

```
python -m src.agent.graph
```

This starts a simple command-line interface:

```
LangGraph-style Math Agent (local). Type 'exit' to quit.
> 
```

---

## Usage Examples

### Mathematical Queries

```
10 - 4
What is 5 plus 3
multiply 4 and 8
divide 16 by 2
subtract 5 from 12
```

### General Queries

```
Who is Albert Einstein
Explain what machine learning is
What is LangGraph
Write a short paragraph about India
```

### Edge Cases

```
How much is 8 divided by 0
Compute 5 times apple   (router fallback)
Tell me something       (LLM)
```

---

## How the Agent Works

### 1. Router

Uses regex to detect if the query contains:

* numeric operators (`+ - * / × ÷`)
* operator words (`plus`, `minus`, `times`, `divide`)
* verb-first patterns (`multiply 4 and 6`)
* reverse operations (`subtract 5 from 10`)

If yes, it attempts to parse the expression into:

```
(a, operator, b)
```

### 2. Tool Executor

After parsing, one of the tool functions executes:

* plus(a, b)
* subtract(a, b)
* multiply(a, b)
* divide(a, b)

### 3. LLM Fallback

If the router cannot detect a math expression, the query is sent to the local LLM through the Ollama wrapper.

### 4. Output Formatting

All math outputs are normalized into:

```
a operator b = result (computed via tool)
```

---

## Future Improvements

* Add LangGraph full graph node definitions and edges.
* Implement a fully structured LangGraph agent with cycles and conditional edges.
* Add support for spelled-out numbers (e.g., “five”, “twenty”).
* Add multi-step expression support (e.g., `(5 + 3) * 2`).
* Add a Streamlit UI.
* Integrate conversation memory for follow-up questions.

---

## Advancements You Can Make

These additions will upgrade this into a more advanced course-ready agent:

1. **Tool registry using LangChain schemas**
2. **LangGraph conditional edges**
3. **Async LLM calls**
4. **Multiple tools: math, date operations, string operations**
5. **Chat history and memory**
6. **Ollama embeddings for retrieval**
7. **UI dashboard for demonstrations**

---

## Conclusion

This project demonstrates the foundation for building AI agents with routing, tool usage, and LLM integration while running entirely on a local system. It is suitable for educational, academic, and offline setups.

You can extend this architecture into full LangGraph-style agents or integrate more tools and capabilities as you progress.

```
