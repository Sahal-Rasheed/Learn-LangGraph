import random
from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    name: str
    number: list[int]
    counter: int


def greeting_node(state: AgentState) -> AgentState:
    """
    A node that adds a greeting message to the state.
    """
    state["message"] = "Hello " + state["name"]
    state["counter"] = 0
    return state


def random_number_node(state: AgentState) -> AgentState:
    """
    A node that generates a list of random numbers.
    """
    state["number"].append(random.randint(1, 10))
    state["counter"] += 1
    return state


def should_continue(state: AgentState) -> str:
    """
    A decision node that checks if we should continue generating numbers.
    """
    if state["counter"] < 5:
        print(f"Counter is {state['counter']}, continuing loop.")
        return "loop"
    else:
        return "exit"


graph = StateGraph(AgentState)
graph.add_node("greeting", greeting_node)
graph.add_node("random_number", random_number_node)

graph.add_edge(START, "greeting")
graph.add_edge("greeting", "random_number")
graph.add_conditional_edges(
    "random_number", # source node or conditional node
    should_continue, # action fn to be performed
    {
        "loop": "random_number", # edge to loop back to same node (random_number)
        "exit": END, # edge to exit the graph
    }
)
app = graph.compile()


if __name__ == "__main__":
    initial_state: AgentState = {"name": "Alice", "number": [], "counter": 0}
    result = app.invoke(initial_state)
    print(result["number"])  # Output: A list of 5 random numbers between 1 and 10
