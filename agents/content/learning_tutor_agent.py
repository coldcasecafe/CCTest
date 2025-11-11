"""Personalized Learning Tutor Agent - Adapts to student needs, tracks progress, generates assessments."""

from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import json


class LearningTutorState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    student_id: str
    subject: str
    progress_tracked: bool
    assessment_generated: bool


@tool
def assess_knowledge_level(student_id: str, subject: str) -> str:
    return json.dumps({
        "student_id": student_id,
        "subject": subject,
        "current_level": "Intermediate",
        "strengths": ["Problem solving", "Theory understanding"],
        "weaknesses": ["Code implementation", "Debugging"],
        "recommended_topics": ["Practical exercises", "Debugging techniques"]
    })


@tool
def generate_practice_problems(topic: str, difficulty: str, count: int = 5) -> str:
    return json.dumps({
        "topic": topic,
        "difficulty": difficulty,
        "problems": [
            {"id": 1, "question": "Implement a binary search...", "difficulty": "medium"},
            {"id": 2, "question": "Find the longest substring...", "difficulty": "medium"}
        ],
        "estimated_time": "30 minutes"
    })


@tool
def track_student_progress(student_id: str, completed_exercises: list) -> str:
    return json.dumps({
        "total_exercises": 45,
        "completed": 32,
        "success_rate": 87.5,
        "time_spent": "12 hours",
        "mastery_level": "Advanced Beginner",
        "next_milestone": "Intermediate certification"
    })


@tool
def provide_personalized_feedback(student_answer: str, correct_answer: str) -> str:
    return json.dumps({
        "correct": False,
        "score": 65,
        "feedback": "Your approach is on the right track, but consider edge cases.",
        "hints": ["Think about empty inputs", "What happens with negative numbers?"],
        "resources": ["Tutorial: Edge Case Handling", "Video: Input Validation"]
    })


tools = [assess_knowledge_level, generate_practice_problems, track_student_progress, provide_personalized_feedback]


def create_learning_tutor_agent(model):
    model_with_tools = model.bind_tools(tools)
    tools_by_name = {tool.name: tool for tool in tools}

    def agent_node(state: LearningTutorState):
        system_prompt = SystemMessage(content="""You are a personalized learning tutor.
        Adapt to student needs, provide helpful feedback, and track progress.""")
        response = model_with_tools.invoke([system_prompt] + list(state["messages"]))
        return {"messages": [response]}

    def tool_node(state: LearningTutorState):
        from langchain_core.messages import ToolMessage
        outputs = []
        for tool_call in state["messages"][-1].tool_calls:
            result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
            outputs.append(ToolMessage(content=str(result), name=tool_call["name"], tool_call_id=tool_call["id"]))
        return {"messages": outputs}

    workflow = StateGraph(LearningTutorState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent",
        lambda s: "tools" if hasattr(s["messages"][-1], "tool_calls") and s["messages"][-1].tool_calls else "end",
        {"tools": "tools", "end": END})
    workflow.add_edge("tools", "agent")

    return workflow.compile(checkpointer=MemorySaver())


if __name__ == "__main__":
    print("Personalized Learning Tutor Agent")
