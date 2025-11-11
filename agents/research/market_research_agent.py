"""
Market Research Agent

Conducts comprehensive market research:
- Competitive intelligence gathering
- Trend analysis
- Market sizing and segmentation
- Report generation with citations
- Continuous monitoring for updates
"""

from typing import Annotated, Sequence, TypedDict, Literal
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import json


class MarketResearchState(TypedDict):
    """State for market research agent"""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    research_topic: str
    sources: list
    findings: list
    report_generated: bool


@tool
def search_competitor_info(company_name: str) -> str:
    """Search for competitor information."""
    return json.dumps({
        "company": company_name,
        "founded": "2018",
        "funding": "$150M Series C",
        "employees": "500-1000",
        "products": ["Product A", "Product B", "Product C"],
        "market_share": "15%",
        "key_differentiators": [
            "AI-powered analytics",
            "Enterprise focus",
            "99.9% uptime SLA"
        ],
        "recent_news": [
            "Launched new ML feature",
            "Expanded to APAC region",
            "Partnership with Fortune 500 company"
        ],
        "pricing": "Enterprise: $999/mo, Business: $499/mo"
    })


@tool
def analyze_market_trends(industry: str, timeframe: str = "6months") -> str:
    """Analyze market trends and patterns."""
    return json.dumps({
        "industry": industry,
        "timeframe": timeframe,
        "trends": [
            {
                "trend": "AI/ML Integration",
                "growth": "+45%",
                "description": "Rapid adoption of AI features",
                "impact": "High",
                "timeframe": "Next 12-18 months"
            },
            {
                "trend": "Privacy-First Solutions",
                "growth": "+32%",
                "description": "Increasing demand for data privacy",
                "impact": "Medium",
                "drivers": ["GDPR", "CCPA", "User awareness"]
            },
            {
                "trend": "API-First Architecture",
                "growth": "+28%",
                "description": "Shift to composable solutions",
                "impact": "High",
                "adoption_rate": "62% of new startups"
            }
        ],
        "market_growth": "18% YoY",
        "total_addressable_market": "$45B"
    })


@tool
def gather_customer_reviews(product_name: str, source: str = "all") -> str:
    """Gather and analyze customer reviews."""
    return json.dumps({
        "product": product_name,
        "total_reviews": 1247,
        "average_rating": 4.2,
        "sentiment_breakdown": {
            "positive": 68,
            "neutral": 22,
            "negative": 10
        },
        "top_positive_themes": [
            {"theme": "Ease of use", "mentions": 456},
            {"theme": "Customer support", "mentions": 342},
            {"theme": "Features", "mentions": 289}
        ],
        "top_negative_themes": [
            {"theme": "Pricing", "mentions": 123},
            {"theme": "Learning curve", "mentions": 89},
            {"theme": "Integration issues", "mentions": 67}
        ],
        "common_use_cases": [
            "E-commerce analytics",
            "Marketing automation",
            "Customer segmentation"
        ]
    })


@tool
def estimate_market_size(industry: str, region: str = "global") -> str:
    """Estimate market size and segmentation."""
    return json.dumps({
        "industry": industry,
        "region": region,
        "total_addressable_market": "$45B",
        "serviceable_available_market": "$12B",
        "serviceable_obtainable_market": "$1.2B",
        "segments": [
            {
                "segment": "Enterprise",
                "size": "$8B",
                "growth_rate": "15%",
                "characteristics": "1000+ employees, complex needs"
            },
            {
                "segment": "Mid-Market",
                "size": "$3B",
                "growth_rate": "22%",
                "characteristics": "100-1000 employees, growing fast"
            },
            {
                "segment": "SMB",
                "size": "$1B",
                "growth_rate": "30%",
                "characteristics": "<100 employees, price sensitive"
            }
        ],
        "geographic_breakdown": {
            "North America": "45%",
            "Europe": "30%",
            "APAC": "20%",
            "Other": "5%"
        }
    })


@tool
def generate_swot_analysis(company_data: dict) -> str:
    """Generate SWOT analysis."""
    return json.dumps({
        "strengths": [
            "Strong brand recognition",
            "Advanced AI capabilities",
            "Large customer base",
            "High customer satisfaction"
        ],
        "weaknesses": [
            "Higher pricing than competitors",
            "Limited presence in APAC",
            "Complex onboarding process"
        ],
        "opportunities": [
            "Emerging markets in APAC",
            "AI/ML trend acceleration",
            "Strategic partnerships",
            "New use cases in healthcare"
        ],
        "threats": [
            "Increasing competition",
            "Price pressure from new entrants",
            "Regulatory changes",
            "Economic downturn"
        ]
    })


@tool
def compile_research_report(findings: list, citations: list) -> str:
    """Compile research findings into a structured report."""
    return json.dumps({
        "report_id": "MKT-RPT-001",
        "status": "Draft",
        "sections": [
            "Executive Summary",
            "Market Overview",
            "Competitive Landscape",
            "Trends & Insights",
            "SWOT Analysis",
            "Recommendations"
        ],
        "page_count": 45,
        "charts_included": 12,
        "citations": len(citations),
        "export_formats": ["PDF", "DOCX", "HTML"]
    })


tools = [
    search_competitor_info,
    analyze_market_trends,
    gather_customer_reviews,
    estimate_market_size,
    generate_swot_analysis,
    compile_research_report
]


def create_market_research_agent(model):
    """Create market research agent."""

    model_with_tools = model.bind_tools(tools)
    tools_by_name = {tool.name: tool for tool in tools}

    def agent_node(state: MarketResearchState):
        system_prompt = SystemMessage(content="""You are a market research analyst.

Your expertise:
- Competitive intelligence gathering
- Market trend analysis
- Customer insight synthesis
- Data-driven reporting
- Strategic recommendations

Research Methodology:
1. Define research questions
2. Gather data from multiple sources
3. Analyze and synthesize findings
4. Identify patterns and insights
5. Generate actionable recommendations
6. Cite all sources

Quality Standards:
- Use multiple data sources for validation
- Distinguish facts from assumptions
- Provide quantitative data when available
- Include confidence levels
- Update findings as new data emerges

Report Guidelines:
- Executive summary first
- Clear structure with sections
- Visual data representation
- Cited sources
- Actionable recommendations
""")

        messages = [system_prompt] + list(state["messages"])
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}

    def tool_node(state: MarketResearchState):
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

    def should_continue(state: MarketResearchState) -> Literal["tools", "end"]:
        last_message = state["messages"][-1]

        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"

        return "end"

    workflow = StateGraph(MarketResearchState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)

    workflow.set_entry_point("agent")

    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {"tools": "tools", "end": END}
    )

    workflow.add_edge("tools", "agent")

    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


def run_market_research_demo():
    """Run demo of market research agent."""
    try:
        from langchain_openai import ChatOpenAI
        model = ChatOpenAI(model="gpt-4o-mini")
    except Exception:
        print("Note: This demo requires OpenAI API key.")
        return

    agent = create_market_research_agent(model)

    config = {"configurable": {"thread_id": "research_001"}}
    initial_state = {
        "messages": [HumanMessage(content="Research the CRM software market and key competitors.")],
        "research_topic": "CRM Software Market",
        "sources": [],
        "findings": [],
        "report_generated": False
    }

    print("Market Research Agent Demo")
    print("=" * 50)

    for event in agent.stream(initial_state, config, stream_mode="values"):
        if "messages" in event:
            last_msg = event["messages"][-1]
            if hasattr(last_msg, "content") and last_msg.content:
                print(f"\n{last_msg.type}: {last_msg.content[:200]}...")


if __name__ == "__main__":
    run_market_research_demo()
