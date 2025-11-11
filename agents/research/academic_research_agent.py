"""Academic Research Assistant Agent - Searches papers, summarizes findings, generates literature reviews."""

from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import json


class AcademicResearchState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    research_question: str
    papers_found: list
    summary_generated: bool


@tool
def search_academic_papers(query: str, database: str = "all") -> str:
    """Search academic databases for papers."""
    return json.dumps({
        "query": query,
        "results": [
            {"title": "Deep Learning for NLP", "authors": ["Smith et al."], "year": 2023,
             "citations": 245, "venue": "ACL", "doi": "10.1234/acl.2023.001"},
            {"title": "Transformer Architectures", "authors": ["Jones et al."], "year": 2022,
             "citations": 892, "venue": "NeurIPS", "doi": "10.1234/neurips.2022.042"}
        ],
        "total_found": 156
    })


@tool
def summarize_paper(paper_id: str) -> str:
    """Generate summary of academic paper."""
    return json.dumps({
        "key_contributions": ["Novel architecture", "SOTA results"],
        "methodology": "Experimental study with benchmarks",
        "findings": "15% improvement over baseline",
        "limitations": ["Limited to English", "Small dataset"],
        "future_work": ["Multilingual extension", "Larger scale study"]
    })


@tool
def identify_research_gaps(papers: list) -> str:
    """Identify gaps in current research."""
    return json.dumps({
        "gaps": [
            "Limited work on low-resource languages",
            "Lack of interpretability studies",
            "Need for real-world deployment studies"
        ]
    })


@tool
def generate_bibliography(papers: list, format: str = "APA") -> str:
    """Generate formatted bibliography."""
    return json.dumps({
        "format": format,
        "entries": [
            "Smith, J., et al. (2023). Deep Learning for NLP. ACL 2023.",
            "Jones, A., et al. (2022). Transformer Architectures. NeurIPS 2022."
        ]
    })


tools = [search_academic_papers, summarize_paper, identify_research_gaps, generate_bibliography]


def create_academic_research_agent(model):
    model_with_tools = model.bind_tools(tools)
    tools_by_name = {tool.name: tool for tool in tools}

    def agent_node(state: AcademicResearchState):
        system_prompt = SystemMessage(content="""You are an academic research assistant.
        Help researchers find papers, summarize findings, identify gaps, and generate literature reviews.""")
        messages = [system_prompt] + list(state["messages"])
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}

    def tool_node(state: AcademicResearchState):
        from langchain_core.messages import ToolMessage
        outputs = []
        for tool_call in state["messages"][-1].tool_calls:
            result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
            outputs.append(ToolMessage(content=str(result), name=tool_call["name"],
                                      tool_call_id=tool_call["id"]))
        return {"messages": outputs}

    workflow = StateGraph(AcademicResearchState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent",
        lambda s: "tools" if hasattr(s["messages"][-1], "tool_calls") and s["messages"][-1].tool_calls else "end",
        {"tools": "tools", "end": END})
    workflow.add_edge("tools", "agent")

    return workflow.compile(checkpointer=MemorySaver())


if __name__ == "__main__":
    print("Academic Research Agent - searches papers, generates literature reviews")
