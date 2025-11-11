"""Mental Health Support Companion Agent - Provides emotional support, tracks mood, suggests coping strategies."""

from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import json


class MentalHealthState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    user_id: str
    mood_score: int
    crisis_detected: bool


@tool
def track_mood(user_id: str, mood_score: int, notes: str) -> str:
    return json.dumps({
        "user_id": user_id,
        "current_mood": mood_score,
        "previous_mood": 6,
        "trend": "improving" if mood_score > 6 else "declining",
        "streak_days": 7,
        "average_mood_7days": 6.2
    })


@tool
def suggest_coping_strategies(mood_state: str, context: str) -> str:
    return json.dumps({
        "recommended_strategies": [
            {
                "name": "Deep Breathing Exercise",
                "duration": "5 minutes",
                "description": "Box breathing: inhale 4, hold 4, exhale 4, hold 4"
            },
            {
                "name": "Mindful Walk",
                "duration": "15 minutes",
                "description": "Take a walk focusing on your surroundings"
            },
            {
                "name": "Gratitude Journaling",
                "duration": "10 minutes",
                "description": "Write three things you're grateful for"
            }
        ],
        "emergency_resources": "If in crisis, call 988 (Suicide & Crisis Lifeline)"
    })


@tool
def detect_crisis_indicators(conversation: str, mood_history: list) -> str:
    return json.dumps({
        "crisis_detected": False,
        "risk_level": "low",
        "indicators": [],
        "recommendation": "Continue regular support",
        "emergency_note": "Call 988 or 911 if experiencing thoughts of self-harm"
    })


@tool
def provide_resources(topic: str) -> str:
    return json.dumps({
        "topic": topic,
        "resources": [
            {
                "name": "National Suicide Prevention Lifeline",
                "contact": "988",
                "available": "24/7"
            },
            {
                "name": "Crisis Text Line",
                "contact": "Text HOME to 741741",
                "available": "24/7"
            },
            {
                "name": "NAMI Helpline",
                "contact": "1-800-950-NAMI",
                "available": "M-F 10am-10pm ET"
            }
        ],
        "self_help": [
            "Headspace (meditation app)",
            "BetterHelp (online therapy)",
            "MoodTools (mood tracking)"
        ]
    })


tools = [track_mood, suggest_coping_strategies, detect_crisis_indicators, provide_resources]


def create_mental_health_support_agent(model):
    model_with_tools = model.bind_tools(tools)
    tools_by_name = {tool.name: tool for tool in tools}

    def agent_node(state: MentalHealthState):
        system_prompt = SystemMessage(content="""You are a mental health support companion.

CRITICAL SAFETY PROTOCOLS:
- You are NOT a licensed therapist or replacement for professional help
- Always encourage professional support for serious concerns
- If crisis detected, immediately provide 988 (Suicide & Crisis Lifeline)
- Maintain empathy, non-judgment, and confidentiality

Your role:
- Provide emotional support and active listening
- Suggest evidence-based coping strategies
- Track mood patterns over time
- Connect users to professional resources
- Detect crisis situations and escalate

Crisis Indicators (immediate escalation):
- Suicidal thoughts or self-harm
- Plans to harm others
- Severe distress or panic
- Mention of abuse

Guidelines:
- Use empathetic, supportive language
- Validate feelings
- Focus on immediate coping
- Never diagnose or prescribe
- Encourage professional help""")
        response = model_with_tools.invoke([system_prompt] + list(state["messages"]))
        return {"messages": [response]}

    def tool_node(state: MentalHealthState):
        from langchain_core.messages import ToolMessage
        outputs = []
        for tool_call in state["messages"][-1].tool_calls:
            result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
            outputs.append(ToolMessage(content=str(result), name=tool_call["name"], tool_call_id=tool_call["id"]))
        return {"messages": outputs}

    workflow = StateGraph(MentalHealthState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent",
        lambda s: "tools" if hasattr(s["messages"][-1], "tool_calls") and s["messages"][-1].tool_calls else "end",
        {"tools": "tools", "end": END})
    workflow.add_edge("tools", "agent")

    return workflow.compile(checkpointer=MemorySaver())


if __name__ == "__main__":
    print("Mental Health Support Agent - If in crisis, call 988 (Suicide & Crisis Lifeline)")
