from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages, AnyMessage
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

def chatbot(state: State):
    msgs = state["messages"]

    print("\nState messages:", msgs)

    response = llm.invoke(msgs)

    # Extract text
    if isinstance(response.content, list):
        final_text = "".join(
            part.get("text", "") for part in response.content if isinstance(part, dict)
        )
    else:
        final_text = response.content

    return {"messages": [AIMessage(content=final_text)]}

def sampleNode(state: State):
    print("\nInside SampleNode", state)
    return {"messages": [AIMessage(content="Sample Node Appended")]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("sampleNode", sampleNode)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "sampleNode")
graph_builder.add_edge("sampleNode", END)

graph = graph_builder.compile()

# CORRECT INITIAL STATE
initial_state = {
    "messages": add_messages([], HumanMessage(content="Hi, My name is Ayushi Soni"))
}

updated_state = graph.invoke(initial_state)
print("Updated State:", updated_state)
