# src/agent/graph.py
"""
A minimal agent that routes queries:
 - If the router detects a math query, parse and compute using math_tools.
 - Otherwise forward to Ollama via llm_client.call_llm.

This file behaves as a simple "graph": Input -> Router -> (MathNode | LLMNode) -> Output
"""
from src.utils.router import is_math_query, parse_math_expression
from src.utils.llm_client import call_llm
from src.tools.math_tools import plus, subtract, multiply, divide

def _format_math_result(a, op, b, result):
    return f"{a} {op} {b} = {result} (computed via tool)"

def _safe_compute(a, op, b):
    try:
        if op == "+":
            return plus(a, b)
        if op == "-":
            return subtract(a, b)
        if op == "*":
            return multiply(a, b)
        if op == "/":
            return divide(a, b)
        raise ValueError(f"Unsupported operator: {op}")
    except Exception as e:
        # return friendly error message
        return f"Error computing expression: {e}"

def process_query(text: str) -> str:
    """Main entrypoint for the agent."""
    if is_math_query(text):
        parsed = parse_math_expression(text)
        if parsed is None:
            # fallback: if router said math but parsing failed, call LLM to be safe
            try:
                return call_llm(text)
            except Exception as e:
                return f"Could not parse math expression and LLM call failed: {e}"
        a, op, b = parsed
        result = _safe_compute(a, op, b)
        return _format_math_result(a, op, b, result)
    else:
        # general question: forward to LLM
        return call_llm(text)


if __name__ == "__main__":
    # simple REPL for manual testing
    print("LangGraph-style Math Agent (local). Type 'exit' to quit.")
    while True:
        try:
            q = input("> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break
        if not q:
            continue
        if q.lower() in ("exit", "quit"):
            break
        try:
            out = process_query(q)
        except Exception as e:
            out = f"Agent error: {e}"
        print(out)
