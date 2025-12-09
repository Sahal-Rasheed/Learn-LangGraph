from typing import TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

class AgentState(TypedDict):
    messages: list[HumanMessage]


def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print("AI Response:", response.content)
    state["messages"].append(response.content)
    return state


graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()


if __name__ == "__main__":
    user_input = input("Enter your message: ")
    while user_input != "exit":
        initial_state: AgentState = {
            "messages": [HumanMessage(content=user_input)]
        }
        agent.invoke(initial_state)
        user_input = input("Enter your message: ")