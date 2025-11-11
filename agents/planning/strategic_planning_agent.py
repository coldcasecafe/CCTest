"""Strategic Planning Agent - Facilitates planning sessions, generates scenarios, evaluates options, tracks decisions."""

from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import json


class StrategicPlanningState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    planning_session_id: str
    stakeholders: list
    scenarios_generated: int
    decisions_made: list


@tool
def facilitate_planning_session(topic: str, stakeholders: list) -> str:
    return json.dumps({
        "session_id": "PLAN-2024-Q4",
        "topic": topic,
        "stakeholders": stakeholders,
        "agenda": [
            "Review current state",
            "Define objectives",
            "Generate scenarios",
            "Evaluate options",
            "Make decisions",
            "Define action items"
        ],
        "duration": "2 hours",
        "status": "scheduled"
    })


@tool
def analyze_current_state(domain: str) -> str:
    return json.dumps({
        "domain": domain,
        "current_state": {
            "market_position": "Growing market share in enterprise segment",
            "revenue": "$50M ARR, 45% YoY growth",
            "team_size": 150,
            "key_challenges": [
                "Scaling customer success",
                "Product differentiation",
                "Competition from larger players"
            ],
            "strengths": ["Strong product", "High customer satisfaction", "Innovative features"],
            "weaknesses": ["Limited sales team", "Brand awareness", "Geographic coverage"]
        }
    })


@tool
def generate_strategic_scenarios(context: dict, timeframe: str = "3years") -> str:
    return json.dumps({
        "scenarios": [
            {
                "name": "Aggressive Growth",
                "description": "Rapid expansion through M&A and sales team scale",
                "probability": 0.3,
                "impact": "High",
                "key_assumptions": ["Market continues growth", "Funding available"],
                "outcomes": {
                    "best_case": "$200M ARR by 2027",
                    "worst_case": "Burn rate too high, dilution",
                    "most_likely": "$120M ARR by 2027"
                }
            },
            {
                "name": "Steady Expansion",
                "description": "Organic growth with focus on profitability",
                "probability": 0.5,
                "impact": "Medium",
                "key_assumptions": ["Market remains stable", "Current retention holds"],
                "outcomes": {
                    "best_case": "$100M ARR by 2027",
                    "worst_case": "$70M ARR by 2027",
                    "most_likely": "$85M ARR by 2027"
                }
            },
            {
                "name": "Niche Dominance",
                "description": "Focus on specific vertical, become category leader",
                "probability": 0.2,
                "impact": "High",
                "key_assumptions": ["Vertical has strong growth", "Can defend position"],
                "outcomes": {
                    "best_case": "Market leader in vertical",
                    "worst_case": "Limited total addressable market",
                    "most_likely": "$60M ARR by 2027, 70% market share in niche"
                }
            }
        ]
    })


@tool
def evaluate_strategic_options(scenarios: list, criteria: dict) -> str:
    return json.dumps({
        "evaluation_criteria": ["ROI", "Risk", "Alignment", "Feasibility", "Impact"],
        "weighted_scores": [
            {
                "scenario": "Aggressive Growth",
                "scores": {"ROI": 8, "Risk": 6, "Alignment": 9, "Feasibility": 6, "Impact": 9},
                "weighted_total": 7.6
            },
            {
                "scenario": "Steady Expansion",
                "scores": {"ROI": 7, "Risk": 8, "Alignment": 8, "Feasibility": 9, "Impact": 7},
                "weighted_total": 7.8
            },
            {
                "scenario": "Niche Dominance",
                "scores": {"ROI": 9, "Risk": 7, "Alignment": 7, "Feasibility": 8, "Impact": 8},
                "weighted_total": 7.9
            }
        ],
        "recommendation": "Niche Dominance (highest score), with elements of Steady Expansion"
    })


@tool
def create_action_plan(decisions: list, timeframe: str) -> str:
    return json.dumps({
        "plan_id": "ACTION-Q1-2025",
        "strategic_pillars": ["Market Leadership", "Product Innovation", "Customer Success"],
        "initiatives": [
            {
                "name": "Healthcare Vertical Expansion",
                "owner": "VP Sales",
                "timeline": "Q1-Q2 2025",
                "budget": "$2M",
                "key_results": ["10 healthcare customers", "$5M healthcare ARR"],
                "dependencies": ["Compliance certifications", "Vertical team hiring"]
            },
            {
                "name": "AI-Powered Features",
                "owner": "VP Product",
                "timeline": "Q1-Q3 2025",
                "budget": "$3M",
                "key_results": ["Launch 3 AI features", "20% engagement increase"],
                "dependencies": ["ML team hiring", "Data infrastructure"]
            }
        ],
        "milestones": [
            {"date": "2025-03-31", "target": "Q1 objectives achieved"},
            {"date": "2025-06-30", "target": "50% of annual plan complete"}
        ]
    })


@tool
def track_strategic_progress(plan_id: str) -> str:
    return json.dumps({
        "plan_id": plan_id,
        "overall_progress": 34.5,
        "on_track": True,
        "initiatives_status": {
            "completed": 2,
            "on_track": 5,
            "at_risk": 1,
            "blocked": 0
        },
        "next_review": "2024-11-30",
        "key_achievements": [
            "Launched healthcare product variant",
            "Hired vertical sales team",
            "Achieved HIPAA compliance"
        ],
        "blockers": ["AI feature delayed due to data pipeline issues"]
    })


tools = [facilitate_planning_session, analyze_current_state, generate_strategic_scenarios,
         evaluate_strategic_options, create_action_plan, track_strategic_progress]


def create_strategic_planning_agent(model):
    model_with_tools = model.bind_tools(tools)
    tools_by_name = {tool.name: tool for tool in tools}

    def agent_node(state: StrategicPlanningState):
        system_prompt = SystemMessage(content="""You are a strategic planning facilitator.

Your expertise:
- Facilitate strategic planning sessions
- Analyze current state and market conditions
- Generate and evaluate scenarios
- Guide decision-making processes
- Create actionable strategic plans
- Track progress and outcomes

Planning Frameworks:
- SWOT Analysis
- Scenario Planning
- OKRs (Objectives & Key Results)
- Balanced Scorecard
- Porter's Five Forces
- Blue Ocean Strategy

Planning Process:
1. Assess current state
2. Define vision and objectives
3. Generate strategic scenarios
4. Evaluate options (risks, ROI, feasibility)
5. Make decisions and prioritize
6. Create action plans
7. Track progress and adapt

Best Practices:
- Involve diverse stakeholders
- Use data-driven insights
- Consider multiple scenarios
- Balance short and long-term
- Create measurable outcomes
- Build in review cycles
- Adapt based on results

Always:
- Ask clarifying questions
- Challenge assumptions
- Provide structured frameworks
- Document decisions
- Focus on actionability""")
        response = model_with_tools.invoke([system_prompt] + list(state["messages"]))
        return {"messages": [response]}

    def tool_node(state: StrategicPlanningState):
        from langchain_core.messages import ToolMessage
        outputs = []
        for tool_call in state["messages"][-1].tool_calls:
            result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
            outputs.append(ToolMessage(content=str(result), name=tool_call["name"], tool_call_id=tool_call["id"]))
        return {"messages": outputs}

    workflow = StateGraph(StrategicPlanningState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent",
        lambda s: "tools" if hasattr(s["messages"][-1], "tool_calls") and s["messages"][-1].tool_calls else "end",
        {"tools": "tools", "end": END})
    workflow.add_edge("tools", "agent")

    return workflow.compile(checkpointer=MemorySaver())


if __name__ == "__main__":
    print("Strategic Planning Agent")
