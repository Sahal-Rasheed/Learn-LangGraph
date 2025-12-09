from typing import TypedDict, Annotated, Sequence

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, SystemMessage
 
load_dotenv()

# from langgraph.graph.message import add_messages
# - add_messages is a reducer fn that controls how updates from nodes are combined with the existing state.
# - tells us how to merge new data into the current state, without a reducer updated would have replaced the
# - existing value entirely. ex - messages: Annotated[list, add_messages]

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


@tool
def add(a: int, b: int) -> int:
    # note: docstring is must for a tool, llm uses it to understand tool functionality
    """
    This is an addition function that adds two numbers.
    """
    return a + b


@tool
def subtract(a: int, b: int) -> int:
    """
    This is a subtraction function that subtracts two numbers.
    """
    return a - b


@tool
def multiply(a: int, b: int) -> int:
    """
    This is a multiplication function that multiplies two numbers.
    """
    return a * b

tools = [add, subtract, multiply]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools)


def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content="You are an AI agent that can reason and use tools to answer user queries.")
    response = llm.invoke([system_prompt] + state["messages"])
    return {"messages": [response]} # update state with new message, add_messages reducer (we annotated) will handle appending


def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if not last_message.tool_calls:
        return "end"
    return "continue"


graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)

tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)

graph.add_edge(START, "our_agent")
graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue": "tools",
        "end": END
    }
)

graph.add_edge("tools", "our_agent")
agent = graph.compile()


if __name__ == "__main__":
    inputs = {
        "messages": [
            # ("user", "Add 40 + 12.") # single step tool call
            # ("user", "Add 40 + 12. Add 100 + 25. What is the total sum?") # multi step tool calls (thats y added loop in graph)
            ("user", "What is 15 multiplied by 3, then subtract 10 from the result, and finally add 25 to that result?") # multi
        ]
    }
    print_stream(agent.stream(inputs, stream_mode="values"))