"""
DevOps Troubleshooting Agent

Monitors and troubleshoots:
- System logs and metrics
- Production issues
- Infrastructure problems
- Automated remediation
- Incident escalation
"""

from typing import Annotated, Sequence, TypedDict, Literal
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import json


class DevOpsState(TypedDict):
    """State for DevOps troubleshooting agent"""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    incident_id: str
    service_name: str
    severity: str  # low, medium, high, critical
    auto_remediated: bool
    requires_escalation: bool


@tool
def check_service_health(service_name: str) -> str:
    """Check health status of a service."""
    return json.dumps({
        "service": service_name,
        "status": "degraded",
        "uptime": "99.5%",
        "response_time_ms": 850,
        "error_rate": 2.3,
        "active_instances": 4,
        "healthy_instances": 3
    })


@tool
def analyze_logs(service_name: str, time_range: str = "last_1h") -> str:
    """Analyze service logs for errors."""
    return json.dumps({
        "total_entries": 45230,
        "error_count": 156,
        "warning_count": 423,
        "top_errors": [
            {
                "message": "Connection timeout to database",
                "count": 89,
                "first_seen": "2024-11-11 10:23:15",
                "severity": "high"
            },
            {
                "message": "Memory usage exceeded 90%",
                "count": 34,
                "first_seen": "2024-11-11 11:05:42",
                "severity": "medium"
            }
        ],
        "patterns": ["Spike in errors at 10:23 AM", "Recurring every 15 minutes"]
    })


@tool
def check_infrastructure_metrics(service_name: str) -> str:
    """Check infrastructure metrics."""
    return json.dumps({
        "cpu_usage": 85.3,
        "memory_usage": 92.1,
        "disk_usage": 67.4,
        "network_io": {"in": "125 MB/s", "out": "89 MB/s"},
        "alerts": [
            {"type": "memory", "message": "Memory usage > 90%", "triggered": "5 min ago"},
            {"type": "cpu", "message": "CPU usage > 80%", "triggered": "2 min ago"}
        ]
    })


@tool
def restart_service(service_name: str, instance_id: str = None) -> str:
    """Restart a service or specific instance."""
    return json.dumps({
        "action": "restart",
        "service": service_name,
        "instance": instance_id or "all",
        "status": "success",
        "downtime": "45 seconds",
        "health_check": "passed"
    })


@tool
def scale_service(service_name: str, desired_instances: int) -> str:
    """Scale service to desired number of instances."""
    return json.dumps({
        "action": "scale",
        "service": service_name,
        "previous_instances": 4,
        "desired_instances": desired_instances,
        "current_instances": desired_instances,
        "status": "completed"
    })


@tool
def create_incident_ticket(service_name: str, severity: str, description: str) -> str:
    """Create incident ticket."""
    return json.dumps({
        "incident_id": f"INC-{hash(service_name) % 10000}",
        "service": service_name,
        "severity": severity,
        "status": "Open",
        "assigned_team": "DevOps" if severity in ["low", "medium"] else "SRE",
        "escalated": severity == "critical"
    })


tools = [
    check_service_health,
    analyze_logs,
    check_infrastructure_metrics,
    restart_service,
    scale_service,
    create_incident_ticket
]


def create_devops_troubleshooting_agent(model):
    """Create DevOps troubleshooting agent graph."""

    model_with_tools = model.bind_tools(tools)
    tools_by_name = {tool.name: tool for tool in tools}

    def agent_node(state: DevOpsState):
        system_prompt = SystemMessage(content="""You are a DevOps troubleshooting specialist.

Your role:
- Monitor system health and performance
- Diagnose production issues quickly
- Perform automated remediation when safe
- Escalate critical issues with full context
- Minimize downtime and user impact

Troubleshooting Process:
1. Assess severity and impact
2. Gather relevant logs and metrics
3. Identify root cause
4. Apply remediation (if safe to automate)
5. Verify resolution
6. Document incident

Auto-remediation Guidelines:
- Safe: Restart unhealthy instance, scale up capacity
- Requires approval: Database changes, configuration updates
- Never automate: Data deletion, security changes

Escalate immediately for:
- Data loss or corruption
- Security breaches
- Multi-service outages
- Unknown root causes
""")

        messages = [system_prompt] + list(state["messages"])
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}

    def tool_node(state: DevOpsState):
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

    def should_continue(state: DevOpsState) -> Literal["tools", "escalate", "end"]:
        last_message = state["messages"][-1]

        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"

        if state.get("severity") == "critical" or state.get("requires_escalation"):
            return "escalate"

        return "end"

    def escalate_node(state: DevOpsState):
        msg = HumanMessage(
            content=f"[INCIDENT ESCALATED]\n"
                   f"Incident: {state.get('incident_id')}\n"
                   f"Service: {state.get('service_name')}\n"
                   f"Severity: {state.get('severity').upper()}\n"
                   f"SRE team has been notified."
        )
        return {"messages": [msg]}

    workflow = StateGraph(DevOpsState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.add_node("escalate", escalate_node)

    workflow.set_entry_point("agent")

    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {"tools": "tools", "escalate": "escalate", "end": END}
    )

    workflow.add_edge("tools", "agent")
    workflow.add_edge("escalate", END)

    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


def run_devops_demo():
    """Run a demo of the DevOps troubleshooting agent."""
    try:
        from langchain_openai import ChatOpenAI
        model = ChatOpenAI(model="gpt-4o-mini")
    except Exception:
        print("Note: This demo requires OpenAI API key.")
        return

    agent = create_devops_troubleshooting_agent(model)

    config = {"configurable": {"thread_id": "incident_001"}}
    initial_state = {
        "messages": [HumanMessage(content="API service is showing high error rates and slow response times.")],
        "incident_id": "",
        "service_name": "api-service",
        "severity": "high",
        "auto_remediated": False,
        "requires_escalation": False
    }

    print("DevOps Troubleshooting Agent Demo")
    print("=" * 50)

    for event in agent.stream(initial_state, config, stream_mode="values"):
        if "messages" in event:
            last_msg = event["messages"][-1]
            if hasattr(last_msg, "content") and last_msg.content:
                print(f"\n{last_msg.type}: {last_msg.content[:200]}...")


if __name__ == "__main__":
    run_devops_demo()
