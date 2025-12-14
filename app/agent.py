from __future__ import annotations
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from .tools import search_ux_db, ux_heuristics
from .prompts import SYSTEM_PROMPT
from .config import settings

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

def build_graph():
    llm = ChatOpenAI(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
        temperature=0.2,
    )

    tools = [search_ux_db, ux_heuristics]
    llm_with_tools = llm.bind_tools(tools)

    def assistant_node(state: AgentState):
        # Ensure system prompt is present (once)
        msgs = state["messages"]
        if not msgs or not isinstance(msgs[0], SystemMessage):
            msgs = [SystemMessage(content=SYSTEM_PROMPT)] + msgs
        resp = llm_with_tools.invoke(msgs)
        return {"messages": [resp]}

    tool_node = ToolNode(tools)

    g = StateGraph(AgentState)
    g.add_node("assistant", assistant_node)
    g.add_node("tools", tool_node)

    g.set_entry_point("assistant")

    # If the model requested tool calls -> tools, else end
    g.add_conditional_edges("assistant", tools_condition, {
        "tools": "tools",
        END: END,
    })

    # After tools run, go back to assistant (to incorporate results)
    g.add_edge("tools", "assistant")

    return g.compile()
