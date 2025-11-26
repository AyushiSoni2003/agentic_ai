from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages, AnyMessage
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage

# --- NEW (Persistence) ---
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# ---------- STATE ----------
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


# ---------- NODES ----------
def chatbot(state: State):
    msgs = state["messages"]
    print("\n\n\nState messages:", msgs)

    response = llm.invoke(msgs)

    # Extract text
    if isinstance(response.content, list):
        final_text = "".join(
            part.get("text", "")
            for part in response.content
            if isinstance(part, dict)
        )
    else:
        final_text = response.content

    return {"messages": [AIMessage(content=final_text)]}


def sampleNode(state: State):
    print("\n\n\nInside SampleNode", state)
    return {"messages": [AIMessage(content="Sample Node Appended")]}


# ---------- GRAPH ----------
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("sampleNode", sampleNode)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "sampleNode")
graph_builder.add_edge("sampleNode", END)

# ---------- POSTGRES CHECKPOINTER ----------
DB_URI = "postgresql://postgres:as310103@localhost:5432/langgraph"

# ---------- USE CONTEXT MANAGER ----------
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:

    # optional serializer
    checkpointer.serializer = JsonPlusSerializer(pickle_fallback=True)

    # create tables (run once)
    checkpointer.setup()

    # compile with checkpointing
    graph = graph_builder.compile(checkpointer=checkpointer)

    # initial state
    initial_state = {
        "messages": add_messages([], HumanMessage(content="Hi, What is my name ?"))
    }

    config = {"configurable": {"thread_id": "ayushi_thread_1"}}

    updated_state = graph.invoke(initial_state, config=config)
    print("\n\n\nUpdated State:", updated_state)

    # show history
    history = graph.get_state_history(config)
    print("\n\n\n--- CHECKPOINT HISTORY ---")
    for h in history:
        print("\nState:", h.values, "| Next:", h.next)