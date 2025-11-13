# langgraph_module/nodes.py
from typing import Dict, Any

# ---------------------------------------------------
# Fake LLM wrapper (replace with real LLM client)
# ---------------------------------------------------
class FakeLLM:
    def run(self, prompt: str) -> str:
        if "summarize" in prompt.lower():
            return "Summary: LangGraph is a graph-based agent framework."
        return "Response: " + prompt[:100]


# ---------------------------------------------------
# BASIC NODES
# ---------------------------------------------------
def read_input(state: Dict[str, Any]) -> Dict[str, Any]:
    state = dict(state)
    state.setdefault("input_text", "This is a demo document about LangGraph.")
    return state


def summarize_node(state: Dict[str, Any]) -> Dict[str, Any]:
    state = dict(state)
    llm = FakeLLM()
    summary = llm.run(f"Summarize: {state['input_text']}")
    state["summary"] = summary
    state["needs_tool"] = len(summary) < 20  # simple rule
    return state


def enrich_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    state = dict(state)
    state["summary"] = state.get("summary", "") + " [enriched]"
    state["needs_tool"] = False
    return state


def finalize(state: Dict[str, Any]) -> Dict[str, Any]:
    return {"final_result": state.get("summary", "(no result)")}


# ---------------------------------------------------
# RAG NODES
# ---------------------------------------------------
def retriever(state: Dict[str, Any]) -> Dict[str, Any]:
    state = dict(state)
    state["docs"] = [
        {"id": 1, "text": "LangGraph creates graph-based agent flows."},
        {"id": 2, "text": "Use retrieval to improve LLM reasoning."}
    ]
    return state


def rag_answer(state: Dict[str, Any]) -> Dict[str, Any]:
    state = dict(state)
    llm = FakeLLM()
    context = "\n".join(doc["text"] for doc in state.get("docs", []))
    prompt = f"Use context:\n{context}\nQuestion: {state['input_text']}"
    state["answer"] = llm.run(prompt)
    return state


def validate_answer(state: Dict[str, Any]) -> Dict[str, Any]:
    state = dict(state)
    state["valid"] = "LangGraph" in state.get("answer", "")
    return state
