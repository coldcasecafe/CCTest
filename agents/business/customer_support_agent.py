"""
Customer Support Agent

A stateful agent that handles customer inquiries with:
- Multi-turn conversation context
- Knowledge base access
- Order history lookup
- Human-in-the-loop escalation for complex issues
- Ticket routing to appropriate departments
"""

from typing import Annotated, Sequence, TypedDict, Literal
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import json


# Define the agent state
class CustomerSupportState(TypedDict):
    """State for customer support agent"""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    customer_id: str
    issue_category: str
    escalation_required: bool
    ticket_id: str


# Define tools
@tool
def search_knowledge_base(query: str) -> str:
    """Search the knowledge base for relevant information."""
    # Mock implementation
    kb_data = {
        "shipping": "Standard shipping takes 5-7 business days. Express shipping takes 2-3 business days.",
        "return": "You can return items within 30 days of purchase for a full refund.",
        "account": "To reset your password, go to Settings > Security > Reset Password.",
        "payment": "We accept all major credit cards, PayPal, and Apple Pay."
    }

    for key, value in kb_data.items():
        if key in query.lower():
            return value

    return "I don't have specific information about that. Let me escalate this to a specialist."


@tool
def get_order_history(customer_id: str) -> str:
    """Retrieve customer order history."""
    # Mock implementation
    return json.dumps({
        "orders": [
            {"id": "ORD-001", "date": "2024-01-15", "status": "Delivered", "total": "$99.99"},
            {"id": "ORD-002", "date": "2024-02-20", "status": "In Transit", "total": "$149.99"}
        ],
        "total_orders": 2,
        "customer_since": "2023-06-01"
    })


@tool
def get_order_status(order_id: str) -> str:
    """Get the status of a specific order."""
    # Mock implementation
    statuses = {
        "ORD-001": "Delivered on 2024-01-20",
        "ORD-002": "In transit, expected delivery 2024-02-25"
    }
    return statuses.get(order_id, "Order not found")


@tool
def create_support_ticket(customer_id: str, category: str, description: str) -> str:
    """Create a support ticket for the customer."""
    # Mock implementation
    ticket_id = f"TKT-{hash(customer_id + category) % 10000}"
    return json.dumps({
        "ticket_id": ticket_id,
        "status": "Open",
        "category": category,
        "priority": "Normal",
        "assigned_to": "Support Team"
    })


@tool
def route_to_department(ticket_id: str, department: str) -> str:
    """Route ticket to appropriate department."""
    # Mock implementation
    departments = ["billing", "technical", "shipping", "returns", "general"]
    if department.lower() in departments:
        return f"Ticket {ticket_id} routed to {department.upper()} department"
    return f"Ticket {ticket_id} routed to GENERAL department"


# Collect all tools
tools = [
    search_knowledge_base,
    get_order_history,
    get_order_status,
    create_support_ticket,
    route_to_department
]


def create_customer_support_agent(model):
    """Create a customer support agent graph."""

    # Bind tools to model
    model_with_tools = model.bind_tools(tools)
    tools_by_name = {tool.name: tool for tool in tools}

    # Define agent node
    def agent_node(state: CustomerSupportState):
        system_prompt = SystemMessage(content="""You are a helpful customer support agent.

Your role:
- Assist customers with their inquiries politely and efficiently
- Use available tools to look up information
- Escalate complex issues to human agents when necessary
- Create tickets for issues that need follow-up

Guidelines:
- Always be empathetic and patient
- Provide clear, accurate information
- If you're unsure, say so and offer to escalate
- Keep track of customer context throughout the conversation
""")

        messages = [system_prompt] + list(state["messages"])
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}

    # Define tool execution node
    def tool_node(state: CustomerSupportState):
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

    # Define escalation check node
    def check_escalation(state: CustomerSupportState) -> Literal["escalate", "continue", "end"]:
        """Determine if escalation is needed."""
        last_message = state["messages"][-1]

        # Check if we need to escalate
        if state.get("escalation_required"):
            return "escalate"

        # Check if there are tool calls to execute
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "continue"

        # Otherwise end
        return "end"

    # Define escalation node
    def escalate_to_human(state: CustomerSupportState):
        """Prepare case for human agent."""
        escalation_message = HumanMessage(
            content=f"[SYSTEM] This conversation has been escalated to a human agent. "
                   f"Customer ID: {state.get('customer_id', 'Unknown')}, "
                   f"Category: {state.get('issue_category', 'General')}"
        )
        return {"messages": [escalation_message], "escalation_required": True}

    # Build the graph
    workflow = StateGraph(CustomerSupportState)

    # Add nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.add_node("escalate", escalate_to_human)

    # Set entry point
    workflow.set_entry_point("agent")

    # Add edges
    workflow.add_conditional_edges(
        "agent",
        check_escalation,
        {
            "continue": "tools",
            "escalate": "escalate",
            "end": END
        }
    )

    workflow.add_edge("tools", "agent")
    workflow.add_edge("escalate", END)

    # Compile with memory
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


def run_customer_support_demo():
    """Run a demo of the customer support agent."""
    try:
        from langchain_openai import ChatOpenAI
        model = ChatOpenAI(model="gpt-4o-mini")
    except Exception:
        print("Note: This demo requires OpenAI API key. Set OPENAI_API_KEY environment variable.")
        return

    agent = create_customer_support_agent(model)

    # Example conversation
    config = {"configurable": {"thread_id": "customer_001"}}
    initial_state = {
        "messages": [HumanMessage(content="I want to know the status of my order ORD-002")],
        "customer_id": "CUST-12345",
        "issue_category": "order_status",
        "escalation_required": False,
        "ticket_id": ""
    }

    print("Customer Support Agent Demo")
    print("=" * 50)

    for event in agent.stream(initial_state, config, stream_mode="values"):
        if "messages" in event:
            last_msg = event["messages"][-1]
            if hasattr(last_msg, "content") and last_msg.content:
                print(f"\n{last_msg.type}: {last_msg.content}")


if __name__ == "__main__":
    run_customer_support_demo()
