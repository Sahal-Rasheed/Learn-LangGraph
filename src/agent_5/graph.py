from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    number1: int
    number2: int
    operation: str
    result: str


def adder(state: AgentState) -> AgentState:
    """
    This node adds two numbers.
    """
    state["result"] = state["number1"] + state["number2"]
    return state


def subtractor(state: AgentState) -> AgentState:
    """
    This node subtracts two numbers.
    """
    state["result"] = state["number1"] - state["number2"]
    return state


def decider(state: AgentState) -> AgentState:
    """
    This node decides which operation to perform based on the 'operation' field.
    """
    if state["operation"] == "+":
        return "addition_operation" # return the edge
    
    elif state["operation"] == "-":
        return "subtraction_operation"
    
    else:
        raise ValueError("Unsupported operation")


graph = StateGraph(AgentState)
graph.add_node("add_node", adder)
graph.add_node("subtract_node", subtractor)
# since decider node deosnot return state (which a node should), we use a lambda that returns the state as is like a pass-through
graph.add_node("decide_node", lambda state: state)

graph.add_edge(START, "decide_node") # start -> another way to set entry point (alternative to set_entry_point)
graph.add_conditional_edges( # conditional edges based on the decider node's output
    "decide_node",
    decider,
    {
        # these will be the edge nodes from decide_node based on the operation
        "addition_operation": "add_node",
        "subtraction_operation": "subtract_node",
    }
)
graph.add_edge("add_node", END) # end -> another way to set finish point (alternative to set_finish_point)
graph.add_edge("subtract_node", END) # end -> another way to set finish point (alternative to set_finish_point)
app = graph.compile()


if __name__ == "__main__":
    initial_state: AgentState = {"number1": 10, "number2": 5, "operation": "+", "result": ""}
    result = app.invoke(initial_state)
    print(result["result"])  # Output: 15
