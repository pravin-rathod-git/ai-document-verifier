# backend/app/services/agent_service.py
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver # <-- NEW: The Memory Engine

# Import our existing LLM and RAG logic
from app.core.llm import llm
from app.services.rag_service import query_rag_system

@tool
def search_documents(query: str) -> str:
    """
    ALWAYS use this tool when the user asks about an uploaded document, a person's details, KYC, or specific files.
    """
    return query_rag_system(query)

tools = [search_documents]
llm_with_tools = llm.bind_tools(tools)

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def call_model(state: AgentState):
    # NEW: We inject the system prompt here so the agent always knows its role, 
    # without cluttering the saved memory history.
    system_prompt = SystemMessage(
        content="You are an intelligent KYC and Document Verification Agent. "
                "If the user asks about specific documents, you MUST use the search_documents tool. "
                "Always remember the context of previous messages."
    )
    
    # Combine system prompt with the human's memory history
    messages_to_pass = [system_prompt] + state['messages']
    
    response = llm_with_tools.invoke(messages_to_pass)
    return {"messages": [response]}

# Build the Graph Workflow
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", tools_condition)
workflow.add_edge("tools", "agent")

# NEW: Initialize the memory checkpointer
memory = MemorySaver()

# NEW: Compile the agent WITH memory attached
agent_app = workflow.compile(checkpointer=memory)

def run_agent(user_question: str, session_id: str = "default_user_session") -> str:
    """
    Starts the agent graph. Uses session_id to remember past conversations.
    """
    # Configure the thread (this tells LangGraph which memory bank to open)
    config = {"configurable": {"thread_id": session_id}}
    
    inputs = {"messages": [HumanMessage(content=user_question)]}
    
    # Run the graph using the inputs AND the memory config
    final_state = agent_app.invoke(inputs, config=config)
    
    return final_state["messages"][-1].content