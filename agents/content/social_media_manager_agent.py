"""Social Media Manager Agent - Creates posts, schedules content, monitors engagement, responds to comments."""

from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import json


class SocialMediaState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    platform: str
    posts_scheduled: int
    engagement_monitored: bool


@tool
def create_social_post(message: str, platform: str) -> str:
    return json.dumps({
        "post_id": "POST-123",
        "platform": platform,
        "content": message,
        "hashtags": ["#marketing", "#business"],
        "character_count": len(message),
        "optimal_time": "3:00 PM EST"
    })


@tool
def schedule_posts(posts: list, schedule: dict) -> str:
    return json.dumps({
        "scheduled_count": len(posts),
        "next_post": "2024-11-12 15:00",
        "platforms": ["Twitter", "LinkedIn", "Facebook"]
    })


@tool
def analyze_engagement(post_id: str) -> str:
    return json.dumps({
        "likes": 245,
        "shares": 34,
        "comments": 12,
        "reach": 5600,
        "engagement_rate": "4.3%",
        "sentiment": "positive"
    })


tools = [create_social_post, schedule_posts, analyze_engagement]


def create_social_media_agent(model):
    model_with_tools = model.bind_tools(tools)
    tools_by_name = {tool.name: tool for tool in tools}

    def agent_node(state: SocialMediaState):
        system_prompt = SystemMessage(content="You are a social media manager. Create engaging posts and monitor performance.")
        response = model_with_tools.invoke([system_prompt] + list(state["messages"]))
        return {"messages": [response]}

    def tool_node(state: SocialMediaState):
        from langchain_core.messages import ToolMessage
        outputs = []
        for tool_call in state["messages"][-1].tool_calls:
            result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
            outputs.append(ToolMessage(content=str(result), name=tool_call["name"], tool_call_id=tool_call["id"]))
        return {"messages": outputs}

    workflow = StateGraph(SocialMediaState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent",
        lambda s: "tools" if hasattr(s["messages"][-1], "tool_calls") and s["messages"][-1].tool_calls else "end",
        {"tools": "tools", "end": END})
    workflow.add_edge("tools", "agent")

    return workflow.compile(checkpointer=MemorySaver())


if __name__ == "__main__":
    print("Social Media Manager Agent")
