from typing import TypedDict

from langgraph.graph import StateGraph


class AgentState(TypedDict):
    name: str
    age: str
    final: str


def first_node(state: AgentState) -> AgentState:
    """
    First node of our sequence.
    """
    state["final"] = f"Hi {state['name']}"
    return state


def second_node(state: AgentState) -> AgentState:
    """
    Second node of our sequence.
    """
    state["final"] += f", you are {state['age']} years old."
    return state


graph = StateGraph(AgentState)
graph.add_node("first_node", first_node)
graph.add_node("second_node", second_node)
graph.set_entry_point("first_node") # start
graph.add_edge("first_node", "second_node") # transition or link -> first node to second node
graph.set_finish_point("second_node") # end
app = graph.compile()


if __name__ == "__main__":
    initial_state: AgentState = {"name": "Alice", "age": "30", "final": ""}
    result = app.invoke(initial_state)
    print(result["final"])  # Output: Hi Alice, you are 30 years old.
