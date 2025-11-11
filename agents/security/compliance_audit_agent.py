"""Compliance Audit Agent - Reviews systems for compliance, identifies gaps, generates audit reports."""

from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import json


class ComplianceAuditState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    audit_id: str
    framework: str
    gaps_identified: list
    compliance_score: int


@tool
def scan_compliance_controls(framework: str, systems: list) -> str:
    return json.dumps({
        "framework": framework,
        "total_controls": 114,
        "controls_checked": 114,
        "compliant": 98,
        "non_compliant": 12,
        "not_applicable": 4,
        "compliance_percentage": 86.0,
        "scan_duration": "12 minutes"
    })


@tool
def identify_compliance_gaps(framework: str, findings: dict) -> str:
    return json.dumps({
        "gaps": [
            {
                "control_id": "AC-2",
                "title": "Account Management",
                "issue": "No automated account review process",
                "severity": "high",
                "requirement": "Review accounts quarterly",
                "remediation": "Implement automated review workflow"
            },
            {
                "control_id": "AU-6",
                "title": "Audit Review",
                "issue": "Logs not reviewed regularly",
                "severity": "medium",
                "requirement": "Review security logs weekly",
                "remediation": "Setup SIEM alerts and weekly review process"
            }
        ],
        "total_gaps": 12,
        "by_severity": {"critical": 2, "high": 4, "medium": 5, "low": 1}
    })


@tool
def assess_risk_level(gaps: list, business_impact: str) -> str:
    return json.dumps({
        "overall_risk": "Medium",
        "risk_breakdown": {
            "data_security": "High",
            "access_control": "Medium",
            "audit_logging": "Medium",
            "incident_response": "Low"
        },
        "likelihood": "Possible",
        "impact": "Moderate",
        "risk_score": 6.5
    })


@tool
def generate_remediation_plan(gaps: list) -> str:
    return json.dumps({
        "remediation_items": [
            {
                "gap_id": "AC-2",
                "action": "Implement quarterly account review",
                "owner": "IT Security Team",
                "priority": "High",
                "effort": "2 weeks",
                "cost": "$5,000",
                "target_date": "2024-12-01"
            },
            {
                "gap_id": "AU-6",
                "action": "Setup SIEM and review process",
                "owner": "SecOps Team",
                "priority": "High",
                "effort": "3 weeks",
                "cost": "$15,000",
                "target_date": "2024-12-15"
            }
        ],
        "total_estimated_cost": "$45,000",
        "total_effort": "12 weeks",
        "expected_compliance_improvement": "+10%"
    })


@tool
def track_remediation_progress(audit_id: str) -> str:
    return json.dumps({
        "audit_id": audit_id,
        "total_items": 12,
        "completed": 5,
        "in_progress": 4,
        "not_started": 3,
        "completion_percentage": 41.7,
        "on_track": True,
        "next_review_date": "2024-11-18"
    })


@tool
def generate_compliance_report(audit_id: str, findings: dict) -> str:
    return json.dumps({
        "report_id": f"AUDIT-{audit_id}",
        "framework": "SOC 2 Type II",
        "audit_period": "Q4 2024",
        "compliance_score": 86,
        "certification_ready": False,
        "sections": [
            "Executive Summary",
            "Audit Scope",
            "Methodology",
            "Findings",
            "Risk Assessment",
            "Remediation Plan",
            "Recommendations"
        ],
        "evidence_items": 247,
        "report_status": "Draft",
        "requires_sign_off": ["CISO", "Compliance Officer"]
    })


tools = [scan_compliance_controls, identify_compliance_gaps, assess_risk_level,
         generate_remediation_plan, track_remediation_progress, generate_compliance_report]


def create_compliance_audit_agent(model):
    model_with_tools = model.bind_tools(tools)
    tools_by_name = {tool.name: tool for tool in tools}

    def agent_node(state: ComplianceAuditState):
        system_prompt = SystemMessage(content="""You are a compliance audit specialist.

Your responsibilities:
- Audit systems against compliance frameworks
- Identify gaps and non-compliance issues
- Assess risk levels
- Generate remediation plans
- Track compliance progress
- Produce audit reports

Supported Frameworks:
- SOC 2 (Type I & II)
- ISO 27001
- HIPAA
- PCI DSS
- GDPR
- NIST 800-53

Audit Process:
1. Define scope and framework
2. Scan systems and controls
3. Identify gaps and issues
4. Assess risk and impact
5. Develop remediation plan
6. Track progress
7. Generate compliance report

Severity Levels:
- CRITICAL: Immediate compliance violation, high risk
- HIGH: Significant gap, must fix soon
- MEDIUM: Notable issue, plan remediation
- LOW: Minor improvement opportunity

Always:
- Be thorough and objective
- Cite specific controls
- Provide actionable recommendations
- Track evidence
- Maintain audit trail""")
        response = model_with_tools.invoke([system_prompt] + list(state["messages"]))
        return {"messages": [response]}

    def tool_node(state: ComplianceAuditState):
        from langchain_core.messages import ToolMessage
        outputs = []
        for tool_call in state["messages"][-1].tool_calls:
            result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
            outputs.append(ToolMessage(content=str(result), name=tool_call["name"], tool_call_id=tool_call["id"]))
        return {"messages": outputs}

    workflow = StateGraph(ComplianceAuditState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent",
        lambda s: "tools" if hasattr(s["messages"][-1], "tool_calls") and s["messages"][-1].tool_calls else "end",
        {"tools": "tools", "end": END})
    workflow.add_edge("tools", "agent")

    return workflow.compile(checkpointer=MemorySaver())


if __name__ == "__main__":
    print("Compliance Audit Agent")
