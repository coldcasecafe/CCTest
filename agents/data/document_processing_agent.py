"""Document Processing Agent - Extracts structured data, classifies documents, handles exceptions."""

from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import json


class DocumentProcessingState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    document_id: str
    document_type: str
    extracted_data: dict
    needs_review: bool


@tool
def classify_document(document_path: str) -> str:
    return json.dumps({
        "document_type": "invoice",
        "confidence": 0.95,
        "language": "en",
        "pages": 2
    })


@tool
def extract_structured_data(document_path: str, document_type: str) -> str:
    return json.dumps({
        "invoice_number": "INV-2024-001",
        "date": "2024-11-11",
        "vendor": "Acme Corp",
        "total_amount": 1250.00,
        "line_items": [
            {"description": "Service A", "amount": 1000.00},
            {"description": "Service B", "amount": 250.00}
        ]
    })


@tool
def validate_extracted_data(data: dict, schema: dict) -> str:
    return json.dumps({
        "valid": True,
        "validation_errors": [],
        "completeness": "100%",
        "confidence_score": 0.92
    })


@tool
def route_document(document_id: str, department: str) -> str:
    return json.dumps({
        "document_id": document_id,
        "routed_to": department,
        "status": "delivered",
        "notification_sent": True
    })


tools = [classify_document, extract_structured_data, validate_extracted_data, route_document]


def create_document_processing_agent(model):
    model_with_tools = model.bind_tools(tools)
    tools_by_name = {tool.name: tool for tool in tools}

    def agent_node(state: DocumentProcessingState):
        system_prompt = SystemMessage(content="You are a document processing specialist. Extract, classify, and route documents.")
        response = model_with_tools.invoke([system_prompt] + list(state["messages"]))
        return {"messages": [response]}

    def tool_node(state: DocumentProcessingState):
        from langchain_core.messages import ToolMessage
        outputs = []
        for tool_call in state["messages"][-1].tool_calls:
            result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
            outputs.append(ToolMessage(content=str(result), name=tool_call["name"], tool_call_id=tool_call["id"]))
        return {"messages": outputs}

    workflow = StateGraph(DocumentProcessingState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent",
        lambda s: "tools" if hasattr(s["messages"][-1], "tool_calls") and s["messages"][-1].tool_calls else "end",
        {"tools": "tools", "end": END})
    workflow.add_edge("tools", "agent")

    return workflow.compile(checkpointer=MemorySaver())


if __name__ == "__main__":
    print("Document Processing Agent")
