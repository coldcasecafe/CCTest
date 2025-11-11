"""
LangGraph Agents Frontend
A Streamlit web application for interacting with 20 different LangGraph agents
"""

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
import os
import sys

# Add agents directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agents'))

from agents.agent_catalog import (
    AGENT_CATALOG,
    get_all_categories,
    get_agents_by_category,
    get_agent_by_id
)


# Page configuration
st.set_page_config(
    page_title="LangGraph Agents Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_agent_creator(agent_id: str):
    """Dynamically load agent creation function"""
    agent_module_map = {
        "customer_support": "business.customer_support_agent",
        "sales_qualification": "business.sales_qualification_agent",
        "contract_review": "business.contract_review_agent",
        "code_review": "development.code_review_agent",
        "devops_troubleshooting": "development.devops_troubleshooting_agent",
        "api_integration": "development.api_integration_builder_agent",
        "market_research": "research.market_research_agent",
        "academic_research": "research.academic_research_agent",
        "financial_analysis": "research.financial_analysis_agent",
        "content_production": "content.content_production_agent",
        "social_media": "content.social_media_manager_agent",
        "learning_tutor": "content.learning_tutor_agent",
        "data_pipeline": "data.data_pipeline_orchestrator_agent",
        "document_processing": "data.document_processing_agent",
        "workflow_automation": "data.workflow_automation_agent",
        "medical_triage": "healthcare.medical_triage_agent",
        "mental_health": "healthcare.mental_health_support_agent",
        "security_incident": "security.security_incident_response_agent",
        "compliance_audit": "security.compliance_audit_agent",
        "strategic_planning": "planning.strategic_planning_agent",
    }

    function_map = {
        "customer_support": "create_customer_support_agent",
        "sales_qualification": "create_sales_qualification_agent",
        "contract_review": "create_contract_review_agent",
        "code_review": "create_code_review_agent",
        "devops_troubleshooting": "create_devops_troubleshooting_agent",
        "api_integration": "create_api_integration_agent",
        "market_research": "create_market_research_agent",
        "academic_research": "create_academic_research_agent",
        "financial_analysis": "create_financial_analysis_agent",
        "content_production": "create_content_production_agent",
        "social_media": "create_social_media_agent",
        "learning_tutor": "create_learning_tutor_agent",
        "data_pipeline": "create_data_pipeline_agent",
        "document_processing": "create_document_processing_agent",
        "workflow_automation": "create_workflow_automation_agent",
        "medical_triage": "create_medical_triage_agent",
        "mental_health": "create_mental_health_support_agent",
        "security_incident": "create_security_incident_response_agent",
        "compliance_audit": "create_compliance_audit_agent",
        "strategic_planning": "create_strategic_planning_agent",
    }

    if agent_id not in agent_module_map:
        return None

    module_name = agent_module_map[agent_id]
    function_name = function_map[agent_id]

    try:
        module = __import__(module_name, fromlist=[function_name])
        return getattr(module, function_name)
    except Exception as e:
        st.error(f"Error loading agent: {e}")
        return None


def initialize_session_state():
    """Initialize Streamlit session state"""
    if "selected_agent_id" not in st.session_state:
        st.session_state.selected_agent_id = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = "session_001"
    if "api_key_configured" not in st.session_state:
        st.session_state.api_key_configured = False


def render_sidebar():
    """Render the sidebar with agent selection"""
    with st.sidebar:
        st.title("🤖 Agent Selection")

        # API Key configuration
        st.subheader("⚙️ Configuration")
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=os.getenv("OPENAI_API_KEY", ""),
            help="Enter your OpenAI API key"
        )

        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            st.session_state.api_key_configured = True
            st.success("✅ API Key configured")
        else:
            st.warning("⚠️ Please enter your OpenAI API key to use the agents")

        st.divider()

        # Agent selection by category
        st.subheader("📁 Select an Agent")

        categories = get_all_categories()

        for category in categories:
            with st.expander(f"**{category}**", expanded=(category == "Business")):
                agents = get_agents_by_category(category)

                for agent in agents:
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.write(agent.icon)
                    with col2:
                        if st.button(
                            agent.name,
                            key=f"btn_{agent.id}",
                            use_container_width=True,
                            type="primary" if st.session_state.selected_agent_id == agent.id else "secondary"
                        ):
                            st.session_state.selected_agent_id = agent.id
                            st.session_state.messages = []
                            st.session_state.agent = None
                            st.rerun()

        st.divider()

        # About section
        with st.expander("ℹ️ About"):
            st.markdown("""
            **LangGraph Agents Platform**

            A collection of 20 production-ready AI agents built with LangGraph.

            Each agent demonstrates:
            - Stateful conversations
            - Tool augmentation
            - Human-in-the-loop workflows
            - Production-ready architecture

            Built with ❤️ using LangGraph
            """)


def render_agent_header(agent_info):
    """Render agent information header"""
    col1, col2 = st.columns([1, 10])

    with col1:
        st.markdown(f"<h1>{agent_info.icon}</h1>", unsafe_allow_html=True)

    with col2:
        st.title(agent_info.name)
        st.caption(f"Category: {agent_info.category}")

    st.markdown(agent_info.description)

    # Features
    with st.expander("✨ Features"):
        cols = st.columns(2)
        for idx, feature in enumerate(agent_info.features):
            with cols[idx % 2]:
                st.markdown(f"- {feature}")

    st.divider()


def render_chat_interface(agent_info):
    """Render the chat interface"""

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        if not st.session_state.api_key_configured:
            st.error("Please configure your OpenAI API key in the sidebar first.")
            return

        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Initialize agent if needed
        if st.session_state.agent is None:
            with st.spinner("Initializing agent..."):
                try:
                    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
                    agent_creator = load_agent_creator(agent_info.id)

                    if agent_creator:
                        st.session_state.agent = agent_creator(model)
                    else:
                        st.error("Could not load agent. Please try another agent.")
                        return
                except Exception as e:
                    st.error(f"Error initializing agent: {e}")
                    return

        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Prepare state
                    state = {
                        "messages": [HumanMessage(content=prompt)],
                        **agent_info.initial_state
                    }

                    config = {
                        "configurable": {
                            "thread_id": st.session_state.thread_id
                        }
                    }

                    # Stream agent response
                    response_placeholder = st.empty()
                    full_response = ""

                    for event in st.session_state.agent.stream(state, config, stream_mode="values"):
                        if "messages" in event and len(event["messages"]) > 0:
                            last_message = event["messages"][-1]

                            # Only show AI messages
                            if hasattr(last_message, "content") and last_message.type in ["ai", "assistant"]:
                                content = last_message.content
                                if content and content != full_response:
                                    full_response = content
                                    response_placeholder.markdown(full_response)

                    if not full_response:
                        full_response = "I processed your request. How else can I help?"
                        response_placeholder.markdown(full_response)

                    # Add assistant message to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": full_response
                    })

                except Exception as e:
                    st.error(f"Error getting response: {e}")
                    st.exception(e)


def render_welcome_page():
    """Render welcome page when no agent is selected"""
    st.title("🤖 Welcome to LangGraph Agents Platform")

    st.markdown("""
    ### Choose an agent from the sidebar to get started!

    This platform provides access to **20 specialized AI agents** across different domains:
    """)

    categories = get_all_categories()

    cols = st.columns(2)
    for idx, category in enumerate(categories):
        with cols[idx % 2]:
            st.subheader(f"📁 {category}")
            agents = get_agents_by_category(category)
            for agent in agents:
                st.markdown(f"**{agent.icon} {agent.name}**")
                st.caption(agent.description)
                st.markdown("---")

    st.info("👈 Select an agent from the sidebar to start chatting!")


def main():
    """Main application"""
    initialize_session_state()
    render_sidebar()

    if st.session_state.selected_agent_id:
        agent_info = get_agent_by_id(st.session_state.selected_agent_id)

        if agent_info:
            render_agent_header(agent_info)

            # Clear chat button
            col1, col2, col3 = st.columns([1, 1, 8])
            with col1:
                if st.button("🗑️ Clear Chat"):
                    st.session_state.messages = []
                    st.session_state.agent = None
                    st.rerun()
            with col2:
                if st.button("🔄 New Session"):
                    import uuid
                    st.session_state.thread_id = str(uuid.uuid4())
                    st.session_state.messages = []
                    st.session_state.agent = None
                    st.rerun()

            render_chat_interface(agent_info)
        else:
            st.error("Agent not found")
    else:
        render_welcome_page()


if __name__ == "__main__":
    main()
