"""Data Pipeline Orchestrator Agent - Coordinates ETL workflows, handles failures, validates data quality."""

from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import json


class DataPipelineState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    pipeline_id: str
    steps_completed: list
    data_quality_validated: bool


@tool
def extract_data(source: str, query: str) -> str:
    return json.dumps({
        "source": source,
        "rows_extracted": 15420,
        "columns": 25,
        "extraction_time": "45s",
        "status": "success"
    })


@tool
def transform_data(data: dict, transformations: list) -> str:
    return json.dumps({
        "transformations_applied": transformations,
        "rows_before": 15420,
        "rows_after": 15380,
        "rows_filtered": 40,
        "validation_passed": True
    })


@tool
def validate_data_quality(data: dict, rules: list) -> str:
    return json.dumps({
        "total_checks": 12,
        "passed": 11,
        "failed": 1,
        "issues": [{"rule": "null_check", "column": "email", "failed_rows": 5}],
        "quality_score": 91.6
    })


@tool
def load_data(destination: str, data: dict) -> str:
    return json.dumps({
        "destination": destination,
        "rows_loaded": 15380,
        "load_time": "23s",
        "status": "success"
    })


tools = [extract_data, transform_data, validate_data_quality, load_data]


def create_data_pipeline_agent(model):
    model_with_tools = model.bind_tools(tools)
    tools_by_name = {tool.name: tool for tool in tools}

    def agent_node(state: DataPipelineState):
        system_prompt = SystemMessage(content="You are a data pipeline orchestrator. Coordinate ETL workflows and ensure data quality.")
        response = model_with_tools.invoke([system_prompt] + list(state["messages"]))
        return {"messages": [response]}

    def tool_node(state: DataPipelineState):
        from langchain_core.messages import ToolMessage
        outputs = []
        for tool_call in state["messages"][-1].tool_calls:
            result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
            outputs.append(ToolMessage(content=str(result), name=tool_call["name"], tool_call_id=tool_call["id"]))
        return {"messages": outputs}

    workflow = StateGraph(DataPipelineState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent",
        lambda s: "tools" if hasattr(s["messages"][-1], "tool_calls") and s["messages"][-1].tool_calls else "end",
        {"tools": "tools", "end": END})
    workflow.add_edge("tools", "agent")

    return workflow.compile(checkpointer=MemorySaver())


if __name__ == "__main__":
    print("Data Pipeline Orchestrator Agent")
