# LangGraph Agents Collection

A comprehensive collection of 20 production-ready agents built with the LangGraph framework, covering business, development, research, content, data, healthcare, security, and planning domains.

## Overview

This repository contains fully functional, stateful agents that demonstrate the power of LangGraph for building:
- **Long-running conversations** with context retention
- **Multi-turn interactions** with memory across sessions
- **Human-in-the-loop workflows** for critical decisions
- **Tool-augmented agents** with external system integration
- **Production-ready architectures** with error handling and monitoring

## Agent Categories

### 🏢 Business Agents

#### 1. Customer Support Agent
**File:** `business/customer_support_agent.py`

Handles customer inquiries with multi-turn conversation context, knowledge base access, and escalation workflows.

**Features:**
- Knowledge base search
- Order history lookup
- Ticket creation and routing
- Human escalation for complex issues
- Multi-channel support

**Use Cases:** Customer service, technical support, help desk automation

---

#### 2. Sales Qualification Agent
**File:** `business/sales_qualification_agent.py`

Qualifies leads through conversational engagement using BANT/MEDDIC frameworks.

**Features:**
- Lead scoring (0-100)
- BANT qualification (Budget, Authority, Need, Timeline)
- Demo scheduling
- CRM integration
- Automated lead routing

**Use Cases:** Lead qualification, sales automation, demo booking

---

#### 3. Contract Review & Negotiation Agent
**File:** `business/contract_review_agent.py`

Analyzes contracts for risks, suggests negotiation strategies, and requires legal approval for high-risk items.

**Features:**
- Term extraction and analysis
- Risk identification (critical, high, medium, low)
- SWOT analysis generation
- Version comparison
- Redline document generation
- Legal review workflows

**Use Cases:** Contract analysis, legal review, M&A due diligence

---

### 💻 Development Agents

#### 4. Code Review Agent
**File:** `development/code_review_agent.py`

Analyzes code for bugs, security vulnerabilities, and quality issues with actionable feedback.

**Features:**
- Static code analysis
- Security vulnerability scanning (OWASP Top 10)
- Test coverage analysis
- Refactoring suggestions
- Style guide compliance
- Automated test execution

**Use Cases:** PR reviews, code quality gates, security audits

---

#### 5. DevOps Troubleshooting Agent
**File:** `development/devops_troubleshooting_agent.py`

Monitors systems, diagnoses issues, and performs automated remediation.

**Features:**
- Service health monitoring
- Log analysis and pattern detection
- Infrastructure metrics tracking
- Automated remediation (restarts, scaling)
- Incident ticket creation
- Escalation workflows

**Use Cases:** Production monitoring, incident response, SRE automation

---

#### 6. API Integration Builder Agent
**File:** `development/api_integration_builder_agent.py`

Discovers APIs and generates production-ready integration code.

**Features:**
- OpenAPI/Swagger endpoint discovery
- Client code generation (Python, JavaScript, etc.)
- Authentication handler generation (OAuth2, API keys)
- Error handling and retry logic
- Integration test generation
- Health check monitoring

**Use Cases:** API integration, SDK generation, microservices connectivity

---

### 🔬 Research Agents

#### 7. Market Research Agent
**File:** `research/market_research_agent.py`

Conducts comprehensive market analysis with competitive intelligence and trend analysis.

**Features:**
- Competitor analysis
- Market trend identification
- Customer review synthesis
- Market sizing and segmentation
- SWOT analysis
- Research report generation

**Use Cases:** Competitive intelligence, market analysis, strategic planning

---

#### 8. Academic Research Assistant Agent
**File:** `research/academic_research_agent.py`

Searches academic databases, summarizes papers, and generates literature reviews.

**Features:**
- Multi-database paper search
- Paper summarization
- Research gap identification
- Citation management
- Bibliography generation (APA, MLA, Chicago)
- Literature review synthesis

**Use Cases:** Academic research, literature reviews, paper discovery

---

#### 9. Financial Analysis Agent
**File:** `research/financial_analysis_agent.py`

Monitors markets, analyzes companies, and generates investment theses.

**Features:**
- Real-time stock data retrieval
- Financial statement analysis
- Investment thesis generation
- Risk assessment
- Price alert configuration
- Portfolio tracking

**Use Cases:** Investment research, portfolio management, financial analysis

---

### 📝 Content Agents

#### 10. Content Production Pipeline Agent
**File:** `content/content_production_agent.py`

Plans content strategy, generates drafts, and optimizes for SEO.

**Features:**
- Content idea generation
- Outline creation
- Draft generation with revisions
- SEO optimization
- Readability analysis
- Multi-stakeholder feedback incorporation

**Use Cases:** Content marketing, blog writing, SEO optimization

---

#### 11. Social Media Manager Agent
**File:** `content/social_media_manager_agent.py`

Creates posts, schedules content, and monitors engagement across platforms.

**Features:**
- Multi-platform post creation
- Content scheduling
- Engagement analytics
- Sentiment analysis
- Comment response automation
- Performance optimization

**Use Cases:** Social media management, community engagement, brand monitoring

---

#### 12. Personalized Learning Tutor Agent
**File:** `content/learning_tutor_agent.py`

Adapts teaching to student needs, tracks progress, and generates assessments.

**Features:**
- Knowledge level assessment
- Personalized practice problem generation
- Progress tracking across sessions
- Adaptive difficulty adjustment
- Immediate feedback with explanations
- Resource recommendations

**Use Cases:** Online education, corporate training, skill development

---

### 📊 Data Agents

#### 13. Data Pipeline Orchestrator Agent
**File:** `data/data_pipeline_orchestrator_agent.py`

Coordinates ETL workflows with data quality validation and error handling.

**Features:**
- Extract, Transform, Load orchestration
- Data quality validation
- Error handling and retries
- Pipeline monitoring
- Audit trail maintenance
- Performance optimization

**Use Cases:** ETL workflows, data integration, data warehousing

---

#### 14. Document Processing Agent
**File:** `data/document_processing_agent.py`

Extracts structured data from documents with classification and routing.

**Features:**
- Document type classification
- Structured data extraction (invoices, forms, etc.)
- Data validation against schemas
- Exception handling with human review
- Automated routing
- Learning from corrections

**Use Cases:** Invoice processing, form automation, document digitization

---

#### 15. Workflow Automation Agent
**File:** `data/workflow_automation_agent.py`

Maps and automates business processes across multiple systems.

**Features:**
- Process mapping and documentation
- Multi-system coordination
- Conditional logic handling
- Audit trail creation
- Compliance verification
- Error recovery

**Use Cases:** Business process automation, system integration, compliance workflows

---

### 🏥 Healthcare Agents

#### 16. Medical Triage Assistant Agent
**File:** `healthcare/medical_triage_agent.py`

Gathers symptoms and provides preliminary assessments (NOT medical advice).

**Features:**
- Conversational symptom gathering
- Urgency level assessment
- Preliminary guidance
- Appointment scheduling
- HIPAA-compliant conversations
- Emergency detection and escalation

**Disclaimers:** Not a replacement for professional medical advice. Always consult healthcare professionals.

**Use Cases:** Telehealth triage, appointment scheduling, symptom tracking

---

#### 17. Mental Health Support Companion Agent
**File:** `healthcare/mental_health_support_agent.py`

Provides 24/7 emotional support with mood tracking and coping strategies.

**Features:**
- Active listening and validation
- Mood tracking across sessions
- Evidence-based coping strategy suggestions
- Crisis detection and escalation
- Professional resource connection
- Progress monitoring

**Crisis Resources:** 988 (Suicide & Crisis Lifeline), Crisis Text Line: Text HOME to 741741

**Disclaimers:** Not a licensed therapist. For emergencies, call 988 or 911.

**Use Cases:** Mental wellness support, mood tracking, crisis intervention

---

### 🔒 Security Agents

#### 18. Security Incident Response Agent
**File:** `security/security_incident_response_agent.py`

Monitors threats, investigates alerts, and executes containment procedures.

**Features:**
- Anomaly detection and monitoring
- Alert investigation
- Automated containment
- Forensic evidence collection
- Incident report generation
- Stakeholder notification

**Use Cases:** SOC automation, incident response, threat hunting

---

#### 19. Compliance Audit Agent
**File:** `security/compliance_audit_agent.py`

Reviews systems for compliance gaps and generates audit reports.

**Features:**
- Multi-framework compliance scanning (SOC 2, ISO 27001, HIPAA, PCI DSS, GDPR)
- Gap identification and risk assessment
- Remediation plan generation
- Progress tracking
- Evidence collection
- Audit report generation

**Use Cases:** Compliance audits, certification preparation, risk management

---

### 📋 Planning Agents

#### 20. Strategic Planning Agent
**File:** `planning/strategic_planning_agent.py`

Facilitates planning sessions, generates scenarios, and tracks strategic initiatives.

**Features:**
- Planning session facilitation
- Current state analysis
- Scenario generation and evaluation
- Decision tracking
- Action plan creation (OKRs, KPIs)
- Progress monitoring

**Use Cases:** Strategic planning, OKR setting, business planning

---

## Installation

```bash
# Clone the repository
cd agents

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your-api-key-here"
# or create a .env file
```

## Requirements

- Python 3.9+
- LangGraph
- LangChain
- OpenAI API key (or other LLM provider)

See `requirements.txt` for full dependencies.

## Quick Start

Each agent can be run independently:

```python
from business.customer_support_agent import create_customer_support_agent
from langchain_openai import ChatOpenAI

# Initialize model
model = ChatOpenAI(model="gpt-4o-mini")

# Create agent
agent = create_customer_support_agent(model)

# Run agent
config = {"configurable": {"thread_id": "unique_thread_id"}}
initial_state = {
    "messages": [HumanMessage(content="I need help with my order")],
    "customer_id": "CUST-123",
    # ... other state fields
}

for event in agent.stream(initial_state, config, stream_mode="values"):
    # Process events
    print(event)
```

## Agent Architecture

All agents follow a consistent architecture:

1. **State Definition**: TypedDict defining agent state
2. **Tools**: Function-based tools for external interactions
3. **Agent Node**: LLM-based decision making
4. **Tool Node**: Tool execution
5. **Conditional Edges**: Routing logic
6. **Checkpointing**: State persistence with MemorySaver

### Common Patterns

- **Human-in-the-Loop**: Escalation nodes for critical decisions
- **Memory**: Persistent state across conversations
- **Error Handling**: Retries and fallback mechanisms
- **Monitoring**: Logging and observability
- **Multi-Agent**: Coordination between specialized agents

## Configuration

Each agent supports configuration through:

- **Thread ID**: For conversation persistence
- **State Initialization**: Custom starting state
- **Model Selection**: Any LangChain-compatible LLM
- **Tool Configuration**: Custom tool implementations
- **Checkpointer**: Memory, Postgres, SQLite, etc.

## Testing

Each agent file can be run directly for a demo:

```bash
python business/customer_support_agent.py
python development/code_review_agent.py
# etc.
```

## Production Deployment

For production use:

1. **Replace Mock Tools**: Implement real integrations
2. **Add Authentication**: Secure API access
3. **Configure Checkpointer**: Use Postgres/Redis for persistence
4. **Add Monitoring**: LangSmith integration
5. **Error Handling**: Production-grade error recovery
6. **Rate Limiting**: Protect external APIs
7. **Secrets Management**: Use environment variables or secret managers

## LangGraph Features Demonstrated

- ✅ **Stateful Agents**: Persistent conversation context
- ✅ **Tool Calling**: External system integration
- ✅ **Conditional Edges**: Dynamic routing
- ✅ **Human-in-the-Loop**: Approval workflows
- ✅ **Memory**: Cross-session state
- ✅ **Checkpointing**: Durable execution
- ✅ **Multi-Turn**: Complex conversations
- ✅ **Error Recovery**: Retry and fallback logic

## Contributing

To add new agents:

1. Create a new file in the appropriate category directory
2. Follow the existing agent structure
3. Include mock tools for demo purposes
4. Add documentation to this README
5. Submit a pull request

## License

See LICENSE file

## Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://docs.langchain.com/)
- [LangSmith](https://smith.langchain.com/)

## Support

For issues or questions:
- GitHub Issues: Create an issue in this repository
- LangChain Forum: [https://forum.langchain.com/](https://forum.langchain.com/)

---

**Built with ❤️ using LangGraph**
