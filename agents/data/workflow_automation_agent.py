"""Workflow Automation Agent - Maps processes, coordinates systems, handles conditional logic."""

from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import json


class WorkflowAutomationState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    workflow_id: str
    steps_executed: list
    workflow_status: str


@tool
def map_business_process(process_name: str) -> str:
    return json.dumps({
        "process": process_name,
        "steps": [
            {"step": 1, "action": "Receive form submission", "system": "Web Form"},
            {"step": 2, "action": "Validate data", "system": "Validator"},
            {"step": 3, "action": "Create ticket", "system": "CRM"},
            {"step": 4, "action": "Notify team", "system": "Slack"}
        ],
        "decision_points": 2,
        "estimated_duration": "5 minutes"
    })


@tool
def execute_workflow_step(step_id: int, action: str, parameters: dict) -> str:
    return json.dumps({
        "step_id": step_id,
        "action": action,
        "status": "success",
        "output": {"result": "completed", "data": parameters},
        "execution_time": "2.3s"
    })


@tool
def handle_conditional_logic(condition: str, context: dict) -> str:
    return json.dumps({
        "condition": condition,
        "evaluated": True,
        "branch_taken": "approve_path",
        "reason": "Amount under threshold"
    })


@tool
def create_audit_trail(workflow_id: str, events: list) -> str:
    return json.dumps({
        "workflow_id": workflow_id,
        "events_logged": len(events),
        "audit_trail_id": f"AUDIT-{workflow_id}",
        "compliance_verified": True
    })


tools = [map_business_process, execute_workflow_step, handle_conditional_logic, create_audit_trail]


def create_workflow_automation_agent(model):
    model_with_tools = model.bind_tools(tools)
    tools_by_name = {tool.name: tool for tool in tools}

    def agent_node(state: WorkflowAutomationState):
        system_prompt = SystemMessage(content="You are a workflow automation specialist. Orchestrate business processes across systems.")
        response = model_with_tools.invoke([system_prompt] + list(state["messages"]))
        return {"messages": [response]}

    def tool_node(state: WorkflowAutomationState):
        from langchain_core.messages import ToolMessage
        outputs = []
        for tool_call in state["messages"][-1].tool_calls:
            result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
            outputs.append(ToolMessage(content=str(result), name=tool_call["name"], tool_call_id=tool_call["id"]))
        return {"messages": outputs}

    workflow = StateGraph(WorkflowAutomationState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent",
        lambda s: "tools" if hasattr(s["messages"][-1], "tool_calls") and s["messages"][-1].tool_calls else "end",
        {"tools": "tools", "end": END})
    workflow.add_edge("tools", "agent")

    return workflow.compile(checkpointer=MemorySaver())


if __name__ == "__main__":
    print("Workflow Automation Agent")
