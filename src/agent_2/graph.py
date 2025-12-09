from typing import TypedDict

from langgraph.graph import StateGraph


class AgentState(TypedDict):
    values: list[int]
    name: str
    result: str


def process_values(state: AgentState) -> AgentState:
    """
    A node that processes a list of integers and updates the result in the state.
    """
    total = sum(state["values"])
    state["result"] = f"Hello {state['name']}, the sum of your values is {total}."
    return state


graph = StateGraph(AgentState)
graph.add_node("process_values", process_values)
graph.set_entry_point("process_values")
graph.set_finish_point("process_values")
app = graph.compile()


if __name__ == "__main__":
    initial_state: AgentState = {"values": [1, 2, 3, 4, 5], "name": "Bob", "result": ""}
    result = app.invoke(initial_state)
    print(result["result"])  # Output: Hello Bob, the sum of your values is 15.
