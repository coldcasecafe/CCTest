"""
Sales Qualification Agent

Engages with leads to:
- Qualify prospects based on conversation patterns
- Score leads using BANT/MEDDIC frameworks
- Book demos and meetings
- Update CRM with conversation insights
- Route qualified leads to sales team
"""

from typing import Annotated, Sequence, TypedDict, Literal
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import json
from datetime import datetime, timedelta


class SalesQualificationState(TypedDict):
    """State for sales qualification agent"""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    lead_id: str
    lead_score: int  # 0-100
    qualification_criteria: dict
    demo_scheduled: bool
    sales_rep_assigned: str


# Define tools
@tool
def get_lead_info(lead_id: str) -> str:
    """Retrieve lead information from CRM."""
    # Mock implementation
    return json.dumps({
        "lead_id": lead_id,
        "company": "Acme Corp",
        "industry": "SaaS",
        "size": "50-200 employees",
        "source": "Website",
        "previous_interactions": 2,
        "last_contact": "2024-11-01"
    })


@tool
def update_lead_score(lead_id: str, score: int, criteria: dict) -> str:
    """Update lead score in CRM based on qualification criteria."""
    # Mock implementation
    return json.dumps({
        "lead_id": lead_id,
        "previous_score": 45,
        "new_score": score,
        "criteria_met": criteria,
        "updated_at": datetime.now().isoformat()
    })


@tool
def check_calendar_availability(preferred_date: str, duration_minutes: int = 30) -> str:
    """Check calendar availability for demo booking."""
    # Mock implementation
    available_slots = [
        "2024-11-15 10:00 AM",
        "2024-11-15 02:00 PM",
        "2024-11-16 11:00 AM",
        "2024-11-17 03:00 PM"
    ]
    return json.dumps({
        "available_slots": available_slots,
        "duration": f"{duration_minutes} minutes",
        "timezone": "EST"
    })


@tool
def schedule_demo(lead_id: str, datetime_slot: str, attendees: list) -> str:
    """Schedule a product demo."""
    # Mock implementation
    return json.dumps({
        "meeting_id": f"DEMO-{hash(lead_id) % 10000}",
        "datetime": datetime_slot,
        "duration": "30 minutes",
        "attendees": attendees,
        "meeting_link": "https://meet.example.com/demo-12345",
        "calendar_invite_sent": True
    })


@tool
def assign_to_sales_rep(lead_id: str, criteria: dict) -> str:
    """Assign lead to appropriate sales representative."""
    # Mock implementation
    # Route based on company size, industry, etc.
    if criteria.get("company_size", "small") == "enterprise":
        rep = "John Smith (Enterprise)"
    elif criteria.get("industry") == "healthcare":
        rep = "Jane Doe (Healthcare Specialist)"
    else:
        rep = "Mike Johnson (General Sales)"

    return json.dumps({
        "lead_id": lead_id,
        "assigned_to": rep,
        "notification_sent": True,
        "priority": "High" if criteria.get("budget_confirmed") else "Normal"
    })


@tool
def log_qualification_notes(lead_id: str, notes: str) -> str:
    """Log qualification notes to CRM."""
    # Mock implementation
    return json.dumps({
        "lead_id": lead_id,
        "notes_added": True,
        "timestamp": datetime.now().isoformat(),
        "note_preview": notes[:100]
    })


# Collect all tools
tools = [
    get_lead_info,
    update_lead_score,
    check_calendar_availability,
    schedule_demo,
    assign_to_sales_rep,
    log_qualification_notes
]


def create_sales_qualification_agent(model):
    """Create a sales qualification agent graph."""

    # Bind tools to model
    model_with_tools = model.bind_tools(tools)
    tools_by_name = {tool.name: tool for tool in tools}

    # Define agent node
    def agent_node(state: SalesQualificationState):
        system_prompt = SystemMessage(content="""You are a professional sales qualification agent.

Your goals:
- Engage leads in friendly, consultative conversations
- Qualify leads using BANT criteria (Budget, Authority, Need, Timeline)
- Ask strategic questions to understand their needs
- Schedule demos for qualified prospects
- Update lead scores based on responses

Qualification Criteria:
- Budget: Do they have allocated budget?
- Authority: Are they a decision-maker?
- Need: Do they have a clear business need?
- Timeline: When are they looking to implement?

Lead Scoring:
- 80-100: Hot lead, immediate follow-up
- 60-79: Warm lead, schedule demo
- 40-59: Cold lead, nurture campaign
- 0-39: Not qualified, long-term nurture

Be conversational, not interrogative. Build rapport while gathering information.
""")

        messages = [system_prompt] + list(state["messages"])
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}

    # Define tool execution node
    def tool_node(state: SalesQualificationState):
        from langchain_core.messages import ToolMessage

        outputs = []
        last_message = state["messages"][-1]

        for tool_call in last_message.tool_calls:
            tool = tools_by_name[tool_call["name"]]
            result = tool.invoke(tool_call["args"])
            outputs.append(
                ToolMessage(
                    content=str(result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"]
                )
            )

        return {"messages": outputs}

    # Define routing logic
    def should_continue(state: SalesQualificationState) -> Literal["tools", "qualify", "end"]:
        """Determine next step."""
        last_message = state["messages"][-1]

        # Check if there are tool calls to execute
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"

        # Check if we should qualify the lead
        if len(state["messages"]) >= 6:  # After sufficient conversation
            return "qualify"

        return "end"

    # Define qualification node
    def qualify_lead(state: SalesQualificationState):
        """Analyze conversation and qualify the lead."""
        # Mock qualification logic
        # In production, this could use ML/AI to analyze conversation
        score = state.get("lead_score", 50)

        qualification_msg = HumanMessage(
            content=f"[QUALIFICATION SUMMARY]\n"
                   f"Lead Score: {score}/100\n"
                   f"Status: {'Qualified' if score >= 60 else 'Not Qualified'}\n"
                   f"Demo Scheduled: {state.get('demo_scheduled', False)}\n"
                   f"Next Action: {'Sales Rep Assigned' if score >= 60 else 'Nurture Campaign'}"
        )
        return {"messages": [qualification_msg]}

    # Build the graph
    workflow = StateGraph(SalesQualificationState)

    # Add nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.add_node("qualify", qualify_lead)

    # Set entry point
    workflow.set_entry_point("agent")

    # Add edges
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "qualify": "qualify",
            "end": END
        }
    )

    workflow.add_edge("tools", "agent")
    workflow.add_edge("qualify", END)

    # Compile with memory
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


def run_sales_qualification_demo():
    """Run a demo of the sales qualification agent."""
    try:
        from langchain_openai import ChatOpenAI
        model = ChatOpenAI(model="gpt-4o-mini")
    except Exception:
        print("Note: This demo requires OpenAI API key. Set OPENAI_API_KEY environment variable.")
        return

    agent = create_sales_qualification_agent(model)

    # Example conversation
    config = {"configurable": {"thread_id": "lead_001"}}
    initial_state = {
        "messages": [HumanMessage(content="Hi, I'm interested in learning more about your product.")],
        "lead_id": "LEAD-12345",
        "lead_score": 50,
        "qualification_criteria": {},
        "demo_scheduled": False,
        "sales_rep_assigned": ""
    }

    print("Sales Qualification Agent Demo")
    print("=" * 50)

    for event in agent.stream(initial_state, config, stream_mode="values"):
        if "messages" in event:
            last_msg = event["messages"][-1]
            if hasattr(last_msg, "content") and last_msg.content:
                print(f"\n{last_msg.type}: {last_msg.content}")


if __name__ == "__main__":
    run_sales_qualification_demo()
