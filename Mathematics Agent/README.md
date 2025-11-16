# LangGraph Math Agent (Local Ollama Version)

This project implements a simple LangGraph-based agent that can:

1. Detect whether a user query is mathematical.
2. For math queries, call predefined Python functions (plus, subtract, multiply, divide).
3. For general queries, use a local LLM via Ollama (for example: llama3.2:3b).
4. Seamlessly route queries through the graph (router → math node / llm node → output).

The entire project runs locally using:
- Python
- LangGraph
- Ollama (local LLM)
- No paid API keys required

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
  requirements.txt: ""
  README.md: ""
```

