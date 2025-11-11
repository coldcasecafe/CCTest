"""Medical Triage Assistant Agent - Gathers symptoms, provides preliminary assessments, recommends urgency level."""

from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import json


class MedicalTriageState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    patient_id: str
    symptoms: list
    urgency_level: str
    recommendation: str


@tool
def gather_patient_symptoms(patient_responses: dict) -> str:
    return json.dumps({
        "symptoms": ["fever", "cough", "fatigue"],
        "duration": "3 days",
        "severity": "moderate",
        "existing_conditions": ["none"]
    })


@tool
def assess_urgency_level(symptoms: list, patient_history: dict) -> str:
    return json.dumps({
        "urgency_level": "moderate",
        "triage_category": "urgent_care",
        "reasoning": "Symptoms suggest possible infection, but no life-threatening signs",
        "red_flags": [],
        "recommended_timeline": "Seek care within 24 hours"
    })


@tool
def provide_preliminary_guidance(symptoms: list) -> str:
    return json.dumps({
        "guidance": [
            "Monitor temperature every 4 hours",
            "Stay hydrated",
            "Rest as much as possible",
            "Seek immediate care if symptoms worsen"
        ],
        "warning_signs": [
            "Difficulty breathing",
            "Chest pain",
            "High fever over 103°F"
        ],
        "disclaimer": "This is not medical advice. Consult a healthcare professional."
    })


@tool
def book_appointment(patient_id: str, urgency: str, preferred_time: str) -> str:
    return json.dumps({
        "appointment_id": "APPT-12345",
        "scheduled_time": preferred_time,
        "provider": "Dr. Smith",
        "type": "Urgent Care Visit",
        "confirmation_sent": True
    })


tools = [gather_patient_symptoms, assess_urgency_level, provide_preliminary_guidance, book_appointment]


def create_medical_triage_agent(model):
    model_with_tools = model.bind_tools(tools)
    tools_by_name = {tool.name: tool for tool in tools}

    def agent_node(state: MedicalTriageState):
        system_prompt = SystemMessage(content="""You are a medical triage assistant.

IMPORTANT DISCLAIMERS:
- You are NOT a replacement for professional medical advice
- Always encourage patients to seek professional care
- For emergencies, immediately direct to 911 or emergency services
- Maintain HIPAA compliance in all interactions

Your role:
- Gather symptom information through conversational questions
- Assess urgency level based on symptoms
- Provide general wellness guidance
- Schedule appropriate appointments
- Escalate critical cases immediately

Urgency Levels:
- EMERGENCY: Life-threatening, call 911
- URGENT: Needs care within 24 hours
- ROUTINE: Can wait for regular appointment
- INFORMATIONAL: General health questions""")
        response = model_with_tools.invoke([system_prompt] + list(state["messages"]))
        return {"messages": [response]}

    def tool_node(state: MedicalTriageState):
        from langchain_core.messages import ToolMessage
        outputs = []
        for tool_call in state["messages"][-1].tool_calls:
            result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
            outputs.append(ToolMessage(content=str(result), name=tool_call["name"], tool_call_id=tool_call["id"]))
        return {"messages": outputs}

    workflow = StateGraph(MedicalTriageState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent",
        lambda s: "tools" if hasattr(s["messages"][-1], "tool_calls") and s["messages"][-1].tool_calls else "end",
        {"tools": "tools", "end": END})
    workflow.add_edge("tools", "agent")

    return workflow.compile(checkpointer=MemorySaver())


if __name__ == "__main__":
    print("Medical Triage Assistant Agent - NOT a replacement for professional medical advice")
