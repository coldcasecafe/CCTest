"""
API Integration Builder Agent

Discovers and builds API integrations:
- API discovery and documentation
- Generate integration code
- Handle authentication
- Error handling and retries
- Health monitoring
"""

from typing import Annotated, Sequence, TypedDict, Literal
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import json


class APIIntegrationState(TypedDict):
    """State for API integration builder"""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    api_name: str
    api_spec: dict
    integration_code: str
    tests_generated: bool


@tool
def discover_api_endpoints(api_url: str) -> str:
    """Discover API endpoints from OpenAPI/Swagger spec."""
    return json.dumps({
        "api_name": "PaymentAPI",
        "version": "v2.0",
        "base_url": "https://api.example.com/v2",
        "auth_type": "OAuth2",
        "endpoints": [
            {
                "path": "/payments",
                "method": "POST",
                "description": "Create a new payment",
                "parameters": ["amount", "currency", "customer_id"],
                "response": "Payment object"
            },
            {
                "path": "/payments/{id}",
                "method": "GET",
                "description": "Get payment details",
                "parameters": ["id"],
                "response": "Payment object"
            }
        ]
    })


@tool
def generate_client_code(api_spec: dict, language: str = "python") -> str:
    """Generate client code for API integration."""
    code = '''
class PaymentAPIClient:
    def __init__(self, api_key: str, base_url: str = "https://api.example.com/v2"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def create_payment(self, amount: float, currency: str, customer_id: str):
        """Create a new payment."""
        payload = {
            "amount": amount,
            "currency": currency,
            "customer_id": customer_id
        }
        response = self.session.post(f"{self.base_url}/payments", json=payload)
        response.raise_for_status()
        return response.json()

    def get_payment(self, payment_id: str):
        """Get payment details."""
        response = self.session.get(f"{self.base_url}/payments/{payment_id}")
        response.raise_for_status()
        return response.json()
'''
    return json.dumps({"code": code, "language": language, "dependencies": ["requests"]})


@tool
def generate_auth_handler(auth_type: str, api_name: str) -> str:
    """Generate authentication handler code."""
    return json.dumps({
        "auth_type": auth_type,
        "code": """
class OAuth2Handler:
    def __init__(self, client_id: str, client_secret: str, token_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.token = None
        self.token_expiry = None

    def get_token(self):
        if self.token and datetime.now() < self.token_expiry:
            return self.token

        response = requests.post(self.token_url, data={
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        })
        data = response.json()
        self.token = data["access_token"]
        self.token_expiry = datetime.now() + timedelta(seconds=data["expires_in"])
        return self.token
""",
        "setup_required": ["client_id", "client_secret", "token_url"]
    })


@tool
def generate_error_handling(api_name: str) -> str:
    """Generate error handling and retry logic."""
    return json.dumps({
        "code": """
from tenacity import retry, stop_after_attempt, wait_exponential

class APIError(Exception):
    pass

class RateLimitError(APIError):
    pass

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def api_call_with_retry(func):
    try:
        return func()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            raise RateLimitError("Rate limit exceeded")
        elif e.response.status_code >= 500:
            raise APIError(f"Server error: {e}")
        else:
            raise
""",
        "dependencies": ["tenacity", "requests"]
    })


@tool
def generate_integration_tests(api_name: str, endpoints: list) -> str:
    """Generate integration tests."""
    return json.dumps({
        "code": """
import pytest
from unittest.mock import Mock, patch

class TestPaymentAPIClient:
    def test_create_payment_success(self):
        client = PaymentAPIClient("test_key")
        with patch.object(client.session, 'post') as mock_post:
            mock_post.return_value.json.return_value = {"id": "pay_123", "status": "success"}
            result = client.create_payment(100.0, "USD", "cust_123")
            assert result["id"] == "pay_123"

    def test_create_payment_auth_error(self):
        client = PaymentAPIClient("invalid_key")
        with patch.object(client.session, 'post') as mock_post:
            mock_post.return_value.raise_for_status.side_effect = requests.HTTPError()
            with pytest.raises(requests.HTTPError):
                client.create_payment(100.0, "USD", "cust_123")
""",
        "test_coverage": 85,
        "test_count": 8
    })


@tool
def setup_health_check(api_url: str) -> str:
    """Setup API health monitoring."""
    return json.dumps({
        "health_check_code": """
def check_api_health(client):
    try:
        response = client.session.get(f"{client.base_url}/health")
        return response.status_code == 200
    except Exception:
        return False
""",
        "monitoring_config": {
            "check_interval": "60s",
            "alert_on_failure": True,
            "timeout": "5s"
        }
    })


tools = [
    discover_api_endpoints,
    generate_client_code,
    generate_auth_handler,
    generate_error_handling,
    generate_integration_tests,
    setup_health_check
]


def create_api_integration_agent(model):
    """Create API integration builder agent."""

    model_with_tools = model.bind_tools(tools)
    tools_by_name = {tool.name: tool for tool in tools}

    def agent_node(state: APIIntegrationState):
        system_prompt = SystemMessage(content="""You are an API integration specialist.

Your responsibilities:
- Discover and document API endpoints
- Generate production-ready client code
- Implement authentication and error handling
- Create comprehensive tests
- Setup health monitoring

Code Generation Standards:
- Follow language best practices
- Include type hints/annotations
- Add docstrings and comments
- Implement proper error handling
- Use retry logic for transient failures
- Handle rate limiting

Security:
- Never hardcode credentials
- Use environment variables
- Implement token refresh
- Validate SSL certificates
- Sanitize inputs
""")

        messages = [system_prompt] + list(state["messages"])
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}

    def tool_node(state: APIIntegrationState):
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

    def should_continue(state: APIIntegrationState) -> Literal["tools", "end"]:
        last_message = state["messages"][-1]

        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"

        return "end"

    workflow = StateGraph(APIIntegrationState)
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


def run_api_integration_demo():
    """Run a demo of the API integration builder."""
    try:
        from langchain_openai import ChatOpenAI
        model = ChatOpenAI(model="gpt-4o-mini")
    except Exception:
        print("Note: This demo requires OpenAI API key.")
        return

    agent = create_api_integration_agent(model)

    config = {"configurable": {"thread_id": "api_integration_001"}}
    initial_state = {
        "messages": [HumanMessage(content="Build an integration for the Stripe Payment API.")],
        "api_name": "Stripe",
        "api_spec": {},
        "integration_code": "",
        "tests_generated": False
    }

    print("API Integration Builder Demo")
    print("=" * 50)

    for event in agent.stream(initial_state, config, stream_mode="values"):
        if "messages" in event:
            last_msg = event["messages"][-1]
            if hasattr(last_msg, "content") and last_msg.content:
                print(f"\n{last_msg.type}: {last_msg.content[:200]}...")


if __name__ == "__main__":
    run_api_integration_demo()
