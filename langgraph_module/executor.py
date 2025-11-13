# langgraph_module/executor.py
from typing import Dict, List, Callable, Any

END = "__END__"


class Executor:
    def __init__(self, nodes: Dict[str, Callable], edges: Dict[str, List[str]], entry: str, max_loops: int = 3):
        self.nodes = nodes
        self.edges = edges
        self.entry = entry
        self.max_loops = max_loops

    def run(self, initial_state: Dict[str, Any] = None) -> Dict[str, Any]:
        state = dict(initial_state or {})
        current = self.entry
        loop_count = 0

        while True:
            if current == END:
                return state

            fn = self.nodes[current]
            state = fn(state)

            next_nodes = self.edges.get(current, [])
            if not next_nodes:
                return state

            next_node = next_nodes[0]

            if loop_count >= self.max_loops:
                state["loop_limit_reached"] = True
                return state

            current = next_node
            loop_count += 1
