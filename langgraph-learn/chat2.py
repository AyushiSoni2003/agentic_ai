from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Optional , Literal
from langgraph.graph import StateGraph , START , END
from langchain_core.messages import HumanMessage
from google import genai
import os

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=google_api_key)

class State(TypedDict):
    user_query : str
    llm_output: Optional[str]
    is_good: Optional[bool]

def chatbot(state:State):
    print("\n\nChatbot Node",state)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            state["user_query"]
        ]     
    )

    state["llm_output"] = response.text
    return state

# Redirectory node
def evaluate_response(state: State) -> Literal["chatbot","endnode"]:
    # Mark as good if LLM Output exists
    print("\n\nEvaluate Node",state)   
    if state.get("llm_output"):
        return "endnode"
    return "chatbot"

def endnode(state: State):
    print("\n\nEndNode",state)
    print("\n\n")
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("endnode",endnode)
     
graph_builder.add_edge(START,"chatbot")
graph_builder.add_conditional_edges("chatbot",evaluate_response)
graph_builder.add_edge("endnode",END)

graph = graph_builder.compile()

# Initial State
initial_state = {
    "user_query":"Hi, What is 2 + 2?"
}

updated_state = graph.invoke(initial_state)
print("Updated State:", updated_state)