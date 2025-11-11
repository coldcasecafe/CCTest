"""Security Incident Response Agent - Monitors threats, investigates alerts, executes containment, generates reports."""

from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import json


class SecurityIncidentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    incident_id: str
    severity: str
    containment_executed: bool
    forensics_complete: bool


@tool
def detect_security_anomalies(system: str, timeframe: str = "last_1h") -> str:
    return json.dumps({
        "anomalies_detected": 3,
        "alerts": [
            {
                "type": "Unusual Login Pattern",
                "severity": "high",
                "source_ip": "192.168.1.100",
                "timestamp": "2024-11-11 14:23:15",
                "details": "Multiple failed login attempts from new location"
            },
            {
                "type": "Data Exfiltration",
                "severity": "critical",
                "user": "admin@example.com",
                "volume": "2.3 GB",
                "destination": "external-server.com"
            }
        ]
    })


@tool
def investigate_security_alert(alert_id: str) -> str:
    return json.dumps({
        "alert_id": alert_id,
        "investigation_findings": {
            "attack_vector": "Compromised credentials",
            "affected_systems": ["web-server-01", "database-prod"],
            "timeline": "Attack started 2024-11-11 14:15:00",
            "indicators_of_compromise": [
                "Suspicious process: malware.exe",
                "Unauthorized file access: /etc/passwd",
                "Outbound connection to known C&C server"
            ]
        },
        "evidence_collected": ["Logs", "Network traffic", "File hashes"],
        "recommended_actions": ["Isolate affected systems", "Reset credentials", "Block IP"]
    })


@tool
def execute_containment(incident_id: str, actions: list) -> str:
    return json.dumps({
        "incident_id": incident_id,
        "containment_actions": [
            {"action": "Isolated affected server", "status": "completed", "timestamp": "14:30:15"},
            {"action": "Blocked malicious IP", "status": "completed", "timestamp": "14:30:30"},
            {"action": "Disabled compromised accounts", "status": "completed", "timestamp": "14:31:00"}
        ],
        "threat_contained": True,
        "systems_affected": 2,
        "estimated_downtime": "15 minutes"
    })


@tool
def collect_forensic_evidence(systems: list) -> str:
    return json.dumps({
        "evidence_collected": {
            "memory_dumps": 2,
            "disk_images": 1,
            "log_files": 45,
            "network_captures": "2.5 GB"
        },
        "chain_of_custody": "maintained",
        "storage_location": "secure-evidence-vault",
        "hash_values": ["sha256:abc123...", "sha256:def456..."]
    })


@tool
def generate_incident_report(incident_id: str, findings: dict) -> str:
    return json.dumps({
        "report_id": f"SEC-RPT-{incident_id}",
        "sections": [
            "Executive Summary",
            "Timeline of Events",
            "Attack Analysis",
            "Impact Assessment",
            "Containment Actions",
            "Recommendations",
            "Lessons Learned"
        ],
        "status": "Draft",
        "requires_review": True,
        "compliance_notifications_required": ["ISO 27001", "SOC 2"]
    })


@tool
def notify_stakeholders(incident_id: str, severity: str, stakeholders: list) -> str:
    return json.dumps({
        "notifications_sent": len(stakeholders),
        "channels": ["Email", "Slack", "PagerDuty"],
        "message": "Security incident detected and contained",
        "escalated_to": "CISO" if severity == "critical" else "Security Team"
    })


tools = [detect_security_anomalies, investigate_security_alert, execute_containment,
         collect_forensic_evidence, generate_incident_report, notify_stakeholders]


def create_security_incident_response_agent(model):
    model_with_tools = model.bind_tools(tools)
    tools_by_name = {tool.name: tool for tool in tools}

    def agent_node(state: SecurityIncidentState):
        system_prompt = SystemMessage(content="""You are a security incident response specialist.

Your mission:
- Detect and monitor security threats
- Investigate alerts rapidly
- Execute containment procedures
- Preserve forensic evidence
- Generate detailed incident reports
- Coordinate with stakeholders

Incident Response Process:
1. DETECTION: Identify security anomalies
2. ANALYSIS: Investigate and assess severity
3. CONTAINMENT: Isolate affected systems
4. ERADICATION: Remove threat
5. RECOVERY: Restore normal operations
6. LESSONS LEARNED: Document and improve

Severity Levels:
- CRITICAL: Data breach, ransomware, system compromise
- HIGH: Unauthorized access, malware infection
- MEDIUM: Policy violations, suspicious activity
- LOW: Failed login attempts, minor anomalies

Always:
- Act quickly but methodically
- Preserve evidence
- Document everything
- Communicate clearly
- Follow compliance requirements""")
        response = model_with_tools.invoke([system_prompt] + list(state["messages"]))
        return {"messages": [response]}

    def tool_node(state: SecurityIncidentState):
        from langchain_core.messages import ToolMessage
        outputs = []
        for tool_call in state["messages"][-1].tool_calls:
            result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
            outputs.append(ToolMessage(content=str(result), name=tool_call["name"], tool_call_id=tool_call["id"]))
        return {"messages": outputs}

    workflow = StateGraph(SecurityIncidentState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent",
        lambda s: "tools" if hasattr(s["messages"][-1], "tool_calls") and s["messages"][-1].tool_calls else "end",
        {"tools": "tools", "end": END})
    workflow.add_edge("tools", "agent")

    return workflow.compile(checkpointer=MemorySaver())


if __name__ == "__main__":
    print("Security Incident Response Agent")
