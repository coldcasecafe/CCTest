"""
Agent Catalog - Central registry of all available agents
"""

from typing import Dict, List, Callable
from dataclasses import dataclass


@dataclass
class AgentInfo:
    """Information about an agent"""
    id: str
    name: str
    category: str
    description: str
    icon: str
    create_function: Callable
    initial_state: Dict
    features: List[str]


# Agent catalog with all 20 agents
AGENT_CATALOG = {
    # Business Agents
    "customer_support": AgentInfo(
        id="customer_support",
        name="Customer Support Agent",
        category="Business",
        description="Handles customer inquiries with multi-turn conversation context, knowledge base access, and escalation workflows.",
        icon="💬",
        create_function=lambda model: None,  # Will be populated dynamically
        initial_state={
            "customer_id": "",
            "issue_category": "",
            "escalation_required": False,
            "ticket_id": ""
        },
        features=[
            "Knowledge base search",
            "Order history lookup",
            "Ticket creation and routing",
            "Human escalation"
        ]
    ),

    "sales_qualification": AgentInfo(
        id="sales_qualification",
        name="Sales Qualification Agent",
        category="Business",
        description="Qualifies leads through conversational engagement using BANT/MEDDIC frameworks.",
        icon="💼",
        create_function=lambda model: None,
        initial_state={
            "lead_id": "",
            "lead_score": 50,
            "qualification_criteria": {},
            "demo_scheduled": False,
            "sales_rep_assigned": ""
        },
        features=[
            "BANT qualification",
            "Lead scoring (0-100)",
            "Demo scheduling",
            "CRM integration"
        ]
    ),

    "contract_review": AgentInfo(
        id="contract_review",
        name="Contract Review Agent",
        category="Business",
        description="Analyzes contracts for risks, suggests negotiation strategies, and requires legal approval for high-risk items.",
        icon="📄",
        create_function=lambda model: None,
        initial_state={
            "contract_id": "",
            "contract_type": "",
            "risk_level": "unknown",
            "identified_issues": [],
            "requires_legal_review": False,
            "negotiation_points": []
        },
        features=[
            "Risk identification",
            "Term extraction",
            "Version comparison",
            "Legal review workflows"
        ]
    ),

    # Development Agents
    "code_review": AgentInfo(
        id="code_review",
        name="Code Review Agent",
        category="Development",
        description="Analyzes code for bugs, security vulnerabilities, and quality issues with actionable feedback.",
        icon="🔍",
        create_function=lambda model: None,
        initial_state={
            "pr_id": "",
            "files_changed": [],
            "issues_found": [],
            "severity_level": "info",
            "approved": False
        },
        features=[
            "Security scanning",
            "Quality analysis",
            "Test coverage",
            "Refactoring suggestions"
        ]
    ),

    "devops_troubleshooting": AgentInfo(
        id="devops_troubleshooting",
        name="DevOps Troubleshooting Agent",
        category="Development",
        description="Monitors systems, diagnoses issues, and performs automated remediation.",
        icon="🚨",
        create_function=lambda model: None,
        initial_state={
            "incident_id": "",
            "service_name": "",
            "severity": "unknown",
            "auto_remediated": False,
            "requires_escalation": False
        },
        features=[
            "Service monitoring",
            "Log analysis",
            "Auto-remediation",
            "Incident management"
        ]
    ),

    "api_integration": AgentInfo(
        id="api_integration",
        name="API Integration Builder Agent",
        category="Development",
        description="Discovers APIs and generates production-ready integration code.",
        icon="🔌",
        create_function=lambda model: None,
        initial_state={
            "api_name": "",
            "api_spec": {},
            "integration_code": "",
            "tests_generated": False
        },
        features=[
            "API discovery",
            "Code generation",
            "Auth handling",
            "Test generation"
        ]
    ),

    # Research Agents
    "market_research": AgentInfo(
        id="market_research",
        name="Market Research Agent",
        category="Research",
        description="Conducts comprehensive market analysis with competitive intelligence and trend analysis.",
        icon="📊",
        create_function=lambda model: None,
        initial_state={
            "research_topic": "",
            "sources": [],
            "findings": [],
            "report_generated": False
        },
        features=[
            "Competitor analysis",
            "Trend identification",
            "Market sizing",
            "Report generation"
        ]
    ),

    "academic_research": AgentInfo(
        id="academic_research",
        name="Academic Research Agent",
        category="Research",
        description="Searches academic databases, summarizes papers, and generates literature reviews.",
        icon="🎓",
        create_function=lambda model: None,
        initial_state={
            "research_question": "",
            "papers_found": [],
            "summary_generated": False
        },
        features=[
            "Paper search",
            "Summarization",
            "Gap identification",
            "Bibliography generation"
        ]
    ),

    "financial_analysis": AgentInfo(
        id="financial_analysis",
        name="Financial Analysis Agent",
        category="Research",
        description="Monitors markets, analyzes companies, and generates investment theses.",
        icon="💹",
        create_function=lambda model: None,
        initial_state={
            "ticker": "",
            "analysis_type": "",
            "alerts_configured": False
        },
        features=[
            "Stock analysis",
            "Financial metrics",
            "Investment thesis",
            "Price alerts"
        ]
    ),

    # Content Agents
    "content_production": AgentInfo(
        id="content_production",
        name="Content Production Agent",
        category="Content",
        description="Plans content strategy, generates drafts, and optimizes for SEO.",
        icon="✍️",
        create_function=lambda model: None,
        initial_state={
            "content_type": "",
            "draft_version": 0,
            "seo_optimized": False
        },
        features=[
            "Content planning",
            "Draft generation",
            "SEO optimization",
            "Feedback incorporation"
        ]
    ),

    "social_media": AgentInfo(
        id="social_media",
        name="Social Media Manager Agent",
        category="Content",
        description="Creates posts, schedules content, and monitors engagement across platforms.",
        icon="📱",
        create_function=lambda model: None,
        initial_state={
            "platform": "",
            "posts_scheduled": 0,
            "engagement_monitored": False
        },
        features=[
            "Multi-platform posting",
            "Content scheduling",
            "Engagement analytics",
            "Sentiment analysis"
        ]
    ),

    "learning_tutor": AgentInfo(
        id="learning_tutor",
        name="Learning Tutor Agent",
        category="Content",
        description="Adapts teaching to student needs, tracks progress, and generates assessments.",
        icon="👨‍🏫",
        create_function=lambda model: None,
        initial_state={
            "student_id": "",
            "subject": "",
            "progress_tracked": False,
            "assessment_generated": False
        },
        features=[
            "Personalized learning",
            "Progress tracking",
            "Assessment generation",
            "Adaptive difficulty"
        ]
    ),

    # Data Agents
    "data_pipeline": AgentInfo(
        id="data_pipeline",
        name="Data Pipeline Orchestrator Agent",
        category="Data",
        description="Coordinates ETL workflows with data quality validation and error handling.",
        icon="🔄",
        create_function=lambda model: None,
        initial_state={
            "pipeline_id": "",
            "steps_completed": [],
            "data_quality_validated": False
        },
        features=[
            "ETL orchestration",
            "Quality validation",
            "Error handling",
            "Audit trails"
        ]
    ),

    "document_processing": AgentInfo(
        id="document_processing",
        name="Document Processing Agent",
        category="Data",
        description="Extracts structured data from documents with classification and routing.",
        icon="📑",
        create_function=lambda model: None,
        initial_state={
            "document_id": "",
            "document_type": "",
            "extracted_data": {},
            "needs_review": False
        },
        features=[
            "Document classification",
            "Data extraction",
            "Validation",
            "Automated routing"
        ]
    ),

    "workflow_automation": AgentInfo(
        id="workflow_automation",
        name="Workflow Automation Agent",
        category="Data",
        description="Maps and automates business processes across multiple systems.",
        icon="⚙️",
        create_function=lambda model: None,
        initial_state={
            "workflow_id": "",
            "steps_executed": [],
            "workflow_status": ""
        },
        features=[
            "Process mapping",
            "Multi-system coordination",
            "Conditional logic",
            "Audit trails"
        ]
    ),

    # Healthcare Agents
    "medical_triage": AgentInfo(
        id="medical_triage",
        name="Medical Triage Agent",
        category="Healthcare",
        description="Gathers symptoms and provides preliminary assessments (NOT medical advice).",
        icon="🏥",
        create_function=lambda model: None,
        initial_state={
            "patient_id": "",
            "symptoms": [],
            "urgency_level": "",
            "recommendation": ""
        },
        features=[
            "Symptom gathering",
            "Urgency assessment",
            "Preliminary guidance",
            "Appointment booking"
        ]
    ),

    "mental_health": AgentInfo(
        id="mental_health",
        name="Mental Health Support Agent",
        category="Healthcare",
        description="Provides 24/7 emotional support with mood tracking and coping strategies.",
        icon="🧠",
        create_function=lambda model: None,
        initial_state={
            "user_id": "",
            "mood_score": 5,
            "crisis_detected": False
        },
        features=[
            "Emotional support",
            "Mood tracking",
            "Coping strategies",
            "Crisis detection"
        ]
    ),

    # Security Agents
    "security_incident": AgentInfo(
        id="security_incident",
        name="Security Incident Response Agent",
        category="Security",
        description="Monitors threats, investigates alerts, and executes containment procedures.",
        icon="🛡️",
        create_function=lambda model: None,
        initial_state={
            "incident_id": "",
            "severity": "",
            "containment_executed": False,
            "forensics_complete": False
        },
        features=[
            "Threat monitoring",
            "Alert investigation",
            "Containment",
            "Forensic analysis"
        ]
    ),

    "compliance_audit": AgentInfo(
        id="compliance_audit",
        name="Compliance Audit Agent",
        category="Security",
        description="Reviews systems for compliance gaps and generates audit reports.",
        icon="✅",
        create_function=lambda model: None,
        initial_state={
            "audit_id": "",
            "framework": "",
            "gaps_identified": [],
            "compliance_score": 0
        },
        features=[
            "Compliance scanning",
            "Gap identification",
            "Risk assessment",
            "Remediation planning"
        ]
    ),

    # Planning Agents
    "strategic_planning": AgentInfo(
        id="strategic_planning",
        name="Strategic Planning Agent",
        category="Planning",
        description="Facilitates planning sessions, generates scenarios, and tracks strategic initiatives.",
        icon="🎯",
        create_function=lambda model: None,
        initial_state={
            "planning_session_id": "",
            "stakeholders": [],
            "scenarios_generated": 0,
            "decisions_made": []
        },
        features=[
            "Session facilitation",
            "Scenario planning",
            "Option evaluation",
            "Progress tracking"
        ]
    ),
}


def get_agent_by_id(agent_id: str) -> AgentInfo:
    """Get agent info by ID"""
    return AGENT_CATALOG.get(agent_id)


def get_agents_by_category(category: str) -> List[AgentInfo]:
    """Get all agents in a category"""
    return [agent for agent in AGENT_CATALOG.values() if agent.category == category]


def get_all_categories() -> List[str]:
    """Get all unique categories"""
    return sorted(list(set(agent.category for agent in AGENT_CATALOG.values())))


def get_all_agents() -> List[AgentInfo]:
    """Get all agents"""
    return list(AGENT_CATALOG.values())
