"""Financial Analysis Agent - Market data monitoring, investment analysis, portfolio tracking."""

from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import json


class FinancialAnalysisState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    ticker: str
    analysis_type: str
    alerts_configured: bool


@tool
def get_stock_data(ticker: str, period: str = "1mo") -> str:
    """Fetch stock market data."""
    return json.dumps({
        "ticker": ticker,
        "current_price": 145.67,
        "change_percent": 2.3,
        "volume": 45000000,
        "market_cap": "2.5T",
        "pe_ratio": 28.5,
        "52week_high": 180.23,
        "52week_low": 120.45
    })


@tool
def analyze_financials(ticker: str) -> str:
    """Analyze company financials."""
    return json.dumps({
        "revenue": "$394B",
        "revenue_growth": "8% YoY",
        "profit_margin": "25.3%",
        "debt_to_equity": 1.57,
        "current_ratio": 1.05,
        "rating": "Strong Buy",
        "key_metrics": {
            "ROE": "47.2%",
            "ROA": "22.1%",
            "FCF": "$92B"
        }
    })


@tool
def generate_investment_thesis(company_data: dict) -> str:
    """Generate investment thesis."""
    return json.dumps({
        "recommendation": "Buy",
        "target_price": 165.00,
        "upside": "13.3%",
        "bull_case": ["Market leadership", "Strong growth", "Innovation"],
        "bear_case": ["Regulatory risks", "Competition", "Valuation"],
        "risk_level": "Medium",
        "time_horizon": "12 months"
    })


@tool
def setup_price_alerts(ticker: str, conditions: dict) -> str:
    """Configure price alerts."""
    return json.dumps({
        "ticker": ticker,
        "alerts": [
            {"type": "price_above", "value": 150, "status": "active"},
            {"type": "price_below", "value": 140, "status": "active"},
            {"type": "volume_spike", "threshold": "2x_avg", "status": "active"}
        ]
    })


tools = [get_stock_data, analyze_financials, generate_investment_thesis, setup_price_alerts]


def create_financial_analysis_agent(model):
    model_with_tools = model.bind_tools(tools)
    tools_by_name = {tool.name: tool for tool in tools}

    def agent_node(state: FinancialAnalysisState):
        system_prompt = SystemMessage(content="""You are a financial analyst.
        Analyze markets, companies, and generate investment insights with risk assessments.""")
        messages = [system_prompt] + list(state["messages"])
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}

    def tool_node(state: FinancialAnalysisState):
        from langchain_core.messages import ToolMessage
        outputs = []
        for tool_call in state["messages"][-1].tool_calls:
            result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
            outputs.append(ToolMessage(content=str(result), name=tool_call["name"],
                                      tool_call_id=tool_call["id"]))
        return {"messages": outputs}

    workflow = StateGraph(FinancialAnalysisState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent",
        lambda s: "tools" if hasattr(s["messages"][-1], "tool_calls") and s["messages"][-1].tool_calls else "end",
        {"tools": "tools", "end": END})
    workflow.add_edge("tools", "agent")

    return workflow.compile(checkpointer=MemorySaver())


if __name__ == "__main__":
    print("Financial Analysis Agent - market monitoring, investment analysis, portfolio tracking")
