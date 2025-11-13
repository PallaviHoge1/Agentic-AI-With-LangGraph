# examples/rag_example.py
from langgraph_module import nodes

def rag_pipeline(query: str, max_refines=2):
    state = {"input_text": query}

    state = nodes.retriever(state)
    state = nodes.rag_answer(state)
    state = nodes.validate_answer(state)

    refines = 0
    while not state["valid"] and refines < max_refines:
        print("Refining...")
        state = nodes.enrich_tool(state)
        state = nodes.rag_answer(state)
        state = nodes.validate_answer(state)
        refines += 1

    return {"answer": state["answer"], "valid": state["valid"]}


if __name__ == "__main__":
    print(rag_pipeline("What is LangGraph?"))
