from typing import TypedDict

from langgraph.graph import StateGraph


class AgentState(TypedDict):
    name: str
    age: str
    skills: list[str]
    result: str


def first_node(state: AgentState) -> AgentState:
    """
    First node of our sequence.
    """
    state["result"] = f"{state['name']}, welcome to the system!"
    return state


def second_node(state: AgentState) -> AgentState:
    """
    Second node of our sequence.
    """
    state["result"] += f" You are {state['age']} years old!"
    return state


def third_node(state: AgentState) -> AgentState:
    """
    Third node of our sequence.
    """
    skills_formatted = ", ".join(state["skills"])
    state["result"] += f" You have skills in: {skills_formatted}."
    return state


graph = StateGraph(AgentState)
graph.add_node("first_node", first_node)
graph.add_node("second_node", second_node)
graph.add_node("third_node", third_node)
graph.set_entry_point("first_node") # start
graph.add_edge("first_node", "second_node") # transition or link -> first node to second node
graph.add_edge("second_node", "third_node") # transition or link -> second node to third node
graph.set_finish_point("third_node") # end
app = graph.compile()


if __name__ == "__main__":
    initial_state: AgentState = {"name": "Alice", "age": "30", "skills": ["Python", "Machine Learning"], "result": ""}
    result = app.invoke(initial_state)
    print(result["result"])  # Output: Alice, welcome to the system! You are 30 years old! You have skills in: Python, Machine Learning.
