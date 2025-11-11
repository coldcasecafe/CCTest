"""Content Production Pipeline Agent - Plans content strategy, generates drafts, incorporates feedback, optimizes for SEO."""

from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import json


class ContentProductionState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    content_type: str
    draft_version: int
    seo_optimized: bool


@tool
def generate_content_ideas(topic: str, audience: str) -> str:
    return json.dumps({
        "ideas": [
            {"title": "10 Ways to Improve...", "angle": "listicle", "keywords": ["productivity", "tips"]},
            {"title": "Complete Guide to...", "angle": "comprehensive", "keywords": ["guide", "tutorial"]}
        ]
    })


@tool
def create_content_outline(title: str, keywords: list) -> str:
    return json.dumps({
        "sections": ["Introduction", "Main Points", "Conclusion"],
        "word_count_target": 1500,
        "keywords_to_include": keywords
    })


@tool
def optimize_for_seo(content: str) -> str:
    return json.dumps({
        "seo_score": 85,
        "improvements": ["Add more keywords", "Improve meta description"],
        "readability": "Grade 8",
        "keyword_density": "2.5%"
    })


tools = [generate_content_ideas, create_content_outline, optimize_for_seo]


def create_content_production_agent(model):
    model_with_tools = model.bind_tools(tools)
    tools_by_name = {tool.name: tool for tool in tools}

    def agent_node(state: ContentProductionState):
        system_prompt = SystemMessage(content="You are a content strategist. Plan, create, and optimize content.")
        response = model_with_tools.invoke([system_prompt] + list(state["messages"]))
        return {"messages": [response]}

    def tool_node(state: ContentProductionState):
        from langchain_core.messages import ToolMessage
        outputs = []
        for tool_call in state["messages"][-1].tool_calls:
            result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
            outputs.append(ToolMessage(content=str(result), name=tool_call["name"], tool_call_id=tool_call["id"]))
        return {"messages": outputs}

    workflow = StateGraph(ContentProductionState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent",
        lambda s: "tools" if hasattr(s["messages"][-1], "tool_calls") and s["messages"][-1].tool_calls else "end",
        {"tools": "tools", "end": END})
    workflow.add_edge("tools", "agent")

    return workflow.compile(checkpointer=MemorySaver())


if __name__ == "__main__":
    print("Content Production Pipeline Agent")
