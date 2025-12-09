from typing import TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

class AgentState(TypedDict):
    messages: list[HumanMessage | AIMessage]


def process(state: AgentState) -> AgentState:
    """
    Process the current state by sending messages to the LLM and appending the response.
    """
    response = llm.invoke(state["messages"])
    state["messages"].append(AIMessage(content=response.content))
    print("AI Response:", response.content)
    return state


graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()


if __name__ == "__main__":
    conversation_history = []
    user_input = input("Enter your message: ")
    while user_input != "exit":
        conversation_history.append(HumanMessage(content=user_input))
        result = agent.invoke({
            "messages": conversation_history
        })
        conversation_history = result["messages"]
        user_input = input("Enter your message: ")
