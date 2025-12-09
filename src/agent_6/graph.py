from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    number1: int
    number2: int
    operation1: str
    number3: int
    number4: int
    operation2: str
    result1: str
    result2: str


def adder_1(state: AgentState) -> AgentState:
    """
    This node adds two numbers.
    """
    state["result1"] = state["number1"] + state["number2"]
    return state


def subtractor_1(state: AgentState) -> AgentState:
    """
    This node subtracts two numbers.
    """
    state["result1"] = state["number1"] - state["number2"]
    return state


def adder_2(state: AgentState) -> AgentState:
    """
    This node adds two numbers.
    """
    state["result2"] = state["number3"] + state["number4"]
    return state


def subtractor_2(state: AgentState) -> AgentState:
    """
    This node subtracts two numbers.
    """
    state["result2"] = state["number3"] - state["number4"]
    return state


def decider1(state: AgentState) -> AgentState:
    """
    This node decides which operation to perform based on the 'operation' field.
    """
    if state["operation1"] == "+":
        return "addition_operation" # return the edge
    
    elif state["operation1"] == "-":
        return "subtraction_operation"
    
    else:
        raise ValueError("Unsupported operation")
    

def decider2(state: AgentState) -> AgentState:
    """
    This node decides which operation to perform based on the 'operation' field.
    """
    if state["operation2"] == "+":
        return "addition_operation_2" # return the edge
    
    elif state["operation2"] == "-":
        return "subtraction_operation_2"
    
    else:
        raise ValueError("Unsupported operation")


graph = StateGraph(AgentState)
graph.add_node("add_node_1", adder_1)
graph.add_node("subtract_node_1", subtractor_1)
graph.add_node("decide_node_1", lambda state: state) # pass through
graph.add_node("add_node_2", adder_2)
graph.add_node("subtract_node_2", subtractor_2)
graph.add_node("decide_node_2", lambda state: state) # pass through

graph.add_edge(START, "decide_node_1") # start
graph.add_conditional_edges(
    "decide_node_1",
    decider1,
    {
        "addition_operation": "add_node_1",
        "subtraction_operation": "subtract_node_1",
    }
)
graph.add_edge("add_node_1", "decide_node_2")
graph.add_edge("subtract_node_1", "decide_node_2")
graph.add_conditional_edges(
    "decide_node_2",
    decider2,
    {
        "addition_operation_2": "add_node_2",
        "subtraction_operation_2": "subtract_node_2",
    }
)
graph.add_edge("add_node_2", END)
graph.add_edge("subtract_node_2", END)
app = graph.compile()


if __name__ == "__main__":
    initial_state: AgentState = {"number1": 10, "number2": 5, "operation1": "+", "number3": 20, "number4": 10, "operation2": "-", "result1": 0, "result2": 0}
    result = app.invoke(initial_state)
    print(result["result1"])  # Output: 15
    print(result["result2"])  # Output: 10
