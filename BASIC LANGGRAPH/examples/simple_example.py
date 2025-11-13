# examples/simple_example.py
from langgraph_module import nodes

def run():
    state = {"input_text": "Explain LangGraph."}

    state = nodes.read_input(state)

    loops = 0
    while True:
        state = nodes.summarize_node(state)

        if state.get("needs_tool"):
            if loops >= 2:
                print("Stopped due to loop limit")
                break
            state = nodes.enrich_tool(state)
            loops += 1
            continue

        out = nodes.finalize(state)
        print("Result:", out)
        break


if __name__ == "__main__":
    run()
