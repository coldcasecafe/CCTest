"""
Code Review & Refactoring Agent

Analyzes code for:
- Bugs and potential issues
- Code quality and best practices
- Refactoring opportunities
- Test coverage
- Security vulnerabilities
"""

from typing import Annotated, Sequence, TypedDict, Literal
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import json


class CodeReviewState(TypedDict):
    """State for code review agent"""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    pr_id: str
    files_changed: list
    issues_found: list
    severity_level: str  # info, warning, error, critical
    approved: bool


@tool
def analyze_code_quality(code: str, language: str) -> str:
    """Analyze code for quality issues."""
    # Mock static analysis
    return json.dumps({
        "quality_score": 75,
        "issues": [
            {
                "type": "complexity",
                "severity": "warning",
                "message": "Function has cyclomatic complexity of 15 (max recommended: 10)",
                "line": 42,
                "suggestion": "Consider breaking down into smaller functions"
            },
            {
                "type": "naming",
                "severity": "info",
                "message": "Variable name 'x' is not descriptive",
                "line": 15,
                "suggestion": "Use descriptive variable names like 'user_count'"
            },
            {
                "type": "duplication",
                "severity": "warning",
                "message": "Code duplication detected (15 lines)",
                "line": 78,
                "suggestion": "Extract into reusable function"
            }
        ],
        "language": language
    })


@tool
def check_security_vulnerabilities(code: str) -> str:
    """Scan code for security vulnerabilities."""
    # Mock security scan
    return json.dumps({
        "vulnerabilities": [
            {
                "type": "SQL Injection",
                "severity": "critical",
                "line": 156,
                "description": "Unsanitized user input in SQL query",
                "recommendation": "Use parameterized queries or ORM"
            },
            {
                "type": "XSS",
                "severity": "high",
                "line": 203,
                "description": "User input rendered without escaping",
                "recommendation": "Use template engine auto-escaping"
            }
        ],
        "security_score": 65,
        "owasp_categories": ["A03:2021 – Injection", "A07:2021 – XSS"]
    })


@tool
def analyze_test_coverage(pr_id: str) -> str:
    """Check test coverage for changed code."""
    # Mock coverage analysis
    return json.dumps({
        "overall_coverage": 78.5,
        "changed_files": {
            "src/user_service.py": {
                "coverage": 85.0,
                "lines_covered": 170,
                "lines_total": 200
            },
            "src/payment.py": {
                "coverage": 45.0,
                "lines_covered": 90,
                "lines_total": 200,
                "warning": "Low coverage - add more tests"
            }
        },
        "missing_tests": [
            "Edge case: empty user input",
            "Error handling: network timeout",
            "Integration: payment gateway failure"
        ]
    })


@tool
def suggest_refactoring(code: str, issues: list) -> str:
    """Suggest refactoring improvements."""
    # Mock refactoring suggestions
    return json.dumps({
        "suggestions": [
            {
                "pattern": "Extract Method",
                "location": "lines 42-78",
                "reason": "High complexity, repeated logic",
                "impact": "Improves readability and testability",
                "example": "def validate_user_input(data): ..."
            },
            {
                "pattern": "Replace Conditional with Polymorphism",
                "location": "lines 120-180",
                "reason": "Multiple if/else checking type",
                "impact": "More maintainable and extensible",
                "example": "Use Strategy pattern for different user types"
            },
            {
                "pattern": "Introduce Parameter Object",
                "location": "line 95",
                "reason": "Function has 8 parameters",
                "impact": "Cleaner API, easier to extend",
                "example": "class UserConfig: ..."
            }
        ]
    })


@tool
def run_automated_tests(pr_id: str) -> str:
    """Run test suite for the PR."""
    # Mock test execution
    return json.dumps({
        "status": "PASSED",
        "total_tests": 247,
        "passed": 245,
        "failed": 2,
        "skipped": 0,
        "duration": "2m 34s",
        "failed_tests": [
            {
                "name": "test_payment_processing_timeout",
                "error": "AssertionError: Expected timeout exception",
                "file": "tests/test_payment.py:156"
            },
            {
                "name": "test_user_deletion_cascade",
                "error": "IntegrityError: Foreign key constraint",
                "file": "tests/test_user.py:203"
            }
        ]
    })


@tool
def check_code_standards(code: str, style_guide: str = "PEP8") -> str:
    """Check adherence to coding standards."""
    # Mock linting
    return json.dumps({
        "style_guide": style_guide,
        "violations": [
            {"line": 12, "rule": "E501", "message": "Line too long (92 > 88 characters)"},
            {"line": 45, "rule": "W291", "message": "Trailing whitespace"},
            {"line": 78, "rule": "E302", "message": "Expected 2 blank lines, found 1"}
        ],
        "total_violations": 3,
        "auto_fixable": 3
    })


tools = [
    analyze_code_quality,
    check_security_vulnerabilities,
    analyze_test_coverage,
    suggest_refactoring,
    run_automated_tests,
    check_code_standards
]


def create_code_review_agent(model):
    """Create a code review agent graph."""

    model_with_tools = model.bind_tools(tools)
    tools_by_name = {tool.name: tool for tool in tools}

    def agent_node(state: CodeReviewState):
        system_prompt = SystemMessage(content="""You are an expert code reviewer.

Your responsibilities:
- Analyze code for bugs, security issues, and quality problems
- Suggest improvements and refactoring opportunities
- Verify test coverage
- Check adherence to coding standards
- Provide constructive, actionable feedback

Review Priorities:
1. CRITICAL: Security vulnerabilities, data loss risks
2. HIGH: Bugs, logic errors, performance issues
3. MEDIUM: Code quality, maintainability, test coverage
4. LOW: Style issues, documentation, minor improvements

Guidelines:
- Be specific and provide examples
- Explain the "why" behind suggestions
- Recognize good practices too
- Suggest alternatives when possible
- Consider the broader system context
""")

        messages = [system_prompt] + list(state["messages"])
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}

    def tool_node(state: CodeReviewState):
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

    def should_continue(state: CodeReviewState) -> Literal["tools", "summarize", "end"]:
        last_message = state["messages"][-1]

        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"

        if len(state.get("issues_found", [])) > 0:
            return "summarize"

        return "end"

    def summarize_review(state: CodeReviewState):
        issues = state.get("issues_found", [])
        severity = state.get("severity_level", "info")

        summary_msg = HumanMessage(
            content=f"[CODE REVIEW SUMMARY]\n"
                   f"PR ID: {state.get('pr_id')}\n"
                   f"Files Changed: {len(state.get('files_changed', []))}\n"
                   f"Issues Found: {len(issues)}\n"
                   f"Severity: {severity.upper()}\n"
                   f"Approval: {'❌ Changes Required' if severity in ['error', 'critical'] else '✅ Approved with Comments'}\n"
        )
        return {"messages": [summary_msg], "approved": severity not in ['error', 'critical']}

    # Build the graph
    workflow = StateGraph(CodeReviewState)

    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.add_node("summarize", summarize_review)

    workflow.set_entry_point("agent")

    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "summarize": "summarize",
            "end": END
        }
    )

    workflow.add_edge("tools", "agent")
    workflow.add_edge("summarize", END)

    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


def run_code_review_demo():
    """Run a demo of the code review agent."""
    try:
        from langchain_openai import ChatOpenAI
        model = ChatOpenAI(model="gpt-4o-mini")
    except Exception:
        print("Note: This demo requires OpenAI API key.")
        return

    agent = create_code_review_agent(model)

    config = {"configurable": {"thread_id": "pr_001"}}
    initial_state = {
        "messages": [HumanMessage(content="Please review PR #456 for user authentication feature.")],
        "pr_id": "PR-456",
        "files_changed": ["src/auth.py", "tests/test_auth.py"],
        "issues_found": [],
        "severity_level": "info",
        "approved": False
    }

    print("Code Review Agent Demo")
    print("=" * 50)

    for event in agent.stream(initial_state, config, stream_mode="values"):
        if "messages" in event:
            last_msg = event["messages"][-1]
            if hasattr(last_msg, "content") and last_msg.content:
                print(f"\n{last_msg.type}: {last_msg.content[:200]}...")


if __name__ == "__main__":
    run_code_review_demo()
