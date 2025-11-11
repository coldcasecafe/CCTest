"""
Contract Review & Negotiation Agent

Analyzes contracts for:
- Key terms and obligations
- Risk identification
- Negotiation strategies
- Version control and change tracking
- Human approval workflows for final decisions
"""

from typing import Annotated, Sequence, TypedDict, Literal
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import json


class ContractReviewState(TypedDict):
    """State for contract review agent"""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    contract_id: str
    contract_type: str
    risk_level: str  # low, medium, high, critical
    identified_issues: list
    requires_legal_review: bool
    negotiation_points: list


@tool
def extract_contract_terms(contract_text: str) -> str:
    """Extract key terms from contract."""
    # Mock implementation - would use NLP/LLM for real extraction
    return json.dumps({
        "parties": ["Company A", "Company B"],
        "effective_date": "2024-01-01",
        "termination_date": "2025-01-01",
        "payment_terms": "Net 30",
        "renewal_clause": "Auto-renewal unless 60 days notice",
        "liability_cap": "$1,000,000",
        "governing_law": "Delaware",
        "key_obligations": [
            "Company A will provide software license",
            "Company B will pay monthly fees",
            "Both parties maintain confidentiality"
        ]
    })


@tool
def identify_risks(contract_terms: dict) -> str:
    """Identify potential risks in contract terms."""
    # Mock risk analysis
    risks = [
        {
            "risk": "Unlimited liability",
            "severity": "high",
            "clause": "Section 12.3",
            "recommendation": "Negotiate liability cap"
        },
        {
            "risk": "Auto-renewal without notice period",
            "severity": "medium",
            "clause": "Section 8.1",
            "recommendation": "Request 90-day notice period"
        },
        {
            "risk": "Broad indemnification clause",
            "severity": "high",
            "clause": "Section 15.2",
            "recommendation": "Limit scope of indemnification"
        }
    ]
    return json.dumps({"risks": risks, "overall_risk_level": "high"})


@tool
def compare_contract_versions(contract_id: str, version_a: str, version_b: str) -> str:
    """Compare two versions of a contract to identify changes."""
    # Mock version comparison
    return json.dumps({
        "additions": [
            "Section 14: Added force majeure clause",
            "Section 9.2: Extended warranty period to 24 months"
        ],
        "deletions": [
            "Section 11: Removed non-compete clause"
        ],
        "modifications": [
            "Section 3.1: Payment terms changed from Net 60 to Net 30",
            "Section 7: Liability cap reduced from $5M to $1M"
        ],
        "total_changes": 6
    })


@tool
def suggest_negotiation_points(risks: list, company_priorities: list) -> str:
    """Generate negotiation strategies based on identified risks."""
    # Mock negotiation strategy
    return json.dumps({
        "high_priority": [
            {
                "point": "Liability limitation",
                "current": "Unlimited",
                "target": "$1M cap",
                "rationale": "Protect company from excessive exposure",
                "negotiation_strategy": "Industry standard is capped liability"
            }
        ],
        "medium_priority": [
            {
                "point": "Termination notice period",
                "current": "30 days",
                "target": "90 days",
                "rationale": "Need time for transition",
                "negotiation_strategy": "Operational continuity requirement"
            }
        ],
        "low_priority": [
            {
                "point": "Payment terms",
                "current": "Net 30",
                "target": "Net 45",
                "rationale": "Cash flow management",
                "negotiation_strategy": "Request as goodwill gesture"
            }
        ]
    })


@tool
def generate_redline_document(contract_id: str, changes: list) -> str:
    """Generate a redlined version with proposed changes."""
    # Mock redline generation
    return json.dumps({
        "redline_document_id": f"REDLINE-{contract_id}",
        "changes_count": len(changes),
        "status": "Draft",
        "ready_for_review": True,
        "download_url": f"https://docs.example.com/redline/{contract_id}.pdf"
    })


@tool
def request_legal_approval(contract_id: str, summary: str) -> str:
    """Request approval from legal team."""
    # Mock approval request
    return json.dumps({
        "approval_request_id": f"APPROVAL-{hash(contract_id) % 10000}",
        "assigned_to": "Legal Department",
        "priority": "High",
        "status": "Pending Review",
        "estimated_review_time": "2-3 business days"
    })


tools = [
    extract_contract_terms,
    identify_risks,
    compare_contract_versions,
    suggest_negotiation_points,
    generate_redline_document,
    request_legal_approval
]


def create_contract_review_agent(model):
    """Create a contract review agent graph."""

    model_with_tools = model.bind_tools(tools)
    tools_by_name = {tool.name: tool for tool in tools}

    def agent_node(state: ContractReviewState):
        system_prompt = SystemMessage(content="""You are a contract review specialist.

Your responsibilities:
- Analyze contracts for key terms and obligations
- Identify potential risks and issues
- Suggest negotiation strategies
- Compare contract versions
- Flag contracts requiring legal review

Risk Assessment Criteria:
- CRITICAL: Unlimited liability, non-compete, IP assignment issues
- HIGH: Unfavorable payment terms, weak termination rights, broad indemnification
- MEDIUM: Auto-renewal, long notice periods, warranty limitations
- LOW: Minor administrative terms

Always recommend legal review for CRITICAL and HIGH risk contracts.
Provide clear, actionable recommendations.
""")

        messages = [system_prompt] + list(state["messages"])
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}

    def tool_node(state: ContractReviewState):
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

    def should_continue(state: ContractReviewState) -> Literal["tools", "legal_review", "end"]:
        last_message = state["messages"][-1]

        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"

        if state.get("requires_legal_review") or state.get("risk_level") in ["high", "critical"]:
            return "legal_review"

        return "end"

    def legal_review_node(state: ContractReviewState):
        review_msg = HumanMessage(
            content=f"[LEGAL REVIEW REQUIRED]\n"
                   f"Contract ID: {state.get('contract_id')}\n"
                   f"Risk Level: {state.get('risk_level', 'unknown').upper()}\n"
                   f"Issues Identified: {len(state.get('identified_issues', []))}\n"
                   f"This contract requires human legal review before proceeding."
        )
        return {"messages": [review_msg]}

    # Build the graph
    workflow = StateGraph(ContractReviewState)

    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.add_node("legal_review", legal_review_node)

    workflow.set_entry_point("agent")

    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "legal_review": "legal_review",
            "end": END
        }
    )

    workflow.add_edge("tools", "agent")
    workflow.add_edge("legal_review", END)

    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


def run_contract_review_demo():
    """Run a demo of the contract review agent."""
    try:
        from langchain_openai import ChatOpenAI
        model = ChatOpenAI(model="gpt-4o-mini")
    except Exception:
        print("Note: This demo requires OpenAI API key.")
        return

    agent = create_contract_review_agent(model)

    config = {"configurable": {"thread_id": "contract_001"}}
    initial_state = {
        "messages": [HumanMessage(content="Please review this software license agreement for risks.")],
        "contract_id": "CONTRACT-12345",
        "contract_type": "Software License",
        "risk_level": "unknown",
        "identified_issues": [],
        "requires_legal_review": False,
        "negotiation_points": []
    }

    print("Contract Review Agent Demo")
    print("=" * 50)

    for event in agent.stream(initial_state, config, stream_mode="values"):
        if "messages" in event:
            last_msg = event["messages"][-1]
            if hasattr(last_msg, "content") and last_msg.content:
                print(f"\n{last_msg.type}: {last_msg.content[:200]}...")


if __name__ == "__main__":
    run_contract_review_demo()
