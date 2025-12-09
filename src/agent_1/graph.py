from typing import TypedDict

from langgraph.graph import StateGraph


class AgentState(TypedDict):
    message: str


def greeting_node(state: AgentState) -> AgentState:
    """
    A node that adds a greeting message to the state.
    """
    state["message"] = "Hello " + state["message"] + " how can I assist you today?"
    return state


graph = StateGraph(AgentState)
graph.add_node("greeting", greeting_node)
graph.set_entry_point("greeting")
graph.set_finish_point("greeting")
app = graph.compile()


if __name__ == "__main__":
    # visualize the graph and save as PNG
    # graph_png_buffer = app.get_graph().draw_mermaid_png()
    # with open("graph.png", "wb") as f:
    #     f.write(graph_png_buffer)
    
    # run the app
    initial_state: AgentState = {"message": "Alice"}
    result = app.invoke(initial_state)
    print(result["message"])  # Output: Hello Alice how can I assist you today?
