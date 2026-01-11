from typing import TypedDict, Annotated
import sqlite3
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.sqlite import SqliteSaver

from langchain_core.messages import BaseMessage, SystemMessage
from langchain_ollama import ChatOllama

from tools import TOOLS
from prompt import SYSTEM_PROMPT

load_dotenv()

# Model Setup - Using a larger Qwen model if possible for better tool following
model = ChatOllama(model="qwen3:4b", temperature=0) 
tool_enabled_model = model.bind_tools(TOOLS)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def agent_node(state: ChatState):
    # Filter out redundant system messages if they exist in history
    input_messages = state["messages"]
    full_messages = [SystemMessage(content=SYSTEM_PROMPT)] + input_messages
    
    response = tool_enabled_model.invoke(full_messages)
    return {"messages": [response]}

def route_tools(state: ChatState):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END

# Graph Construction
conn = sqlite3.connect("chatbot.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)

workflow = StateGraph(ChatState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode(TOOLS))

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", route_tools, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent")

chatbot = workflow.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    # Helper to fetch unique thread IDs from DB
    with sqlite3.connect("chatbot.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT thread_id FROM checkpoints")
        return [row[0] for row in cursor.fetchall()] 