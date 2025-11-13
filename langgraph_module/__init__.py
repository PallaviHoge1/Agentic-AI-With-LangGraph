# langgraph_module/__init__.py


"""Simple module initializer for the LangGraph basic scaffold.
Keep imports explicit so `from langgraph_module import executor, nodes` works nicely.
"""


from . import nodes, executor


__all__ = ["nodes", "executor"]