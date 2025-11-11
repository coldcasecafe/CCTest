# LangGraph Agents Platform

A web-based platform providing access to 20 specialized AI agents built with LangGraph, covering business, development, research, content, data, healthcare, security, and planning domains.

![LangGraph Agents](https://img.shields.io/badge/Agents-20-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)

## 🌟 Features

- **20 Specialized Agents** across 8 different domains
- **Interactive Web Interface** built with Streamlit
- **Stateful Conversations** with persistent memory
- **Tool-Augmented Agents** with external integrations
- **Human-in-the-Loop** workflows for critical decisions
- **Production-Ready** architecture

## 🤖 Available Agents

### Business (3)
- 💬 **Customer Support Agent** - Multi-turn support with escalation
- 💼 **Sales Qualification Agent** - BANT lead scoring
- 📄 **Contract Review Agent** - Risk analysis and negotiation

### Development (3)
- 🔍 **Code Review Agent** - Security scanning and quality analysis
- 🚨 **DevOps Troubleshooting Agent** - Monitoring and auto-remediation
- 🔌 **API Integration Builder Agent** - Code generation and testing

### Research (3)
- 📊 **Market Research Agent** - Competitive intelligence
- 🎓 **Academic Research Agent** - Paper search and lit reviews
- 💹 **Financial Analysis Agent** - Investment analysis

### Content (3)
- ✍️ **Content Production Agent** - Strategy and SEO optimization
- 📱 **Social Media Manager Agent** - Multi-platform scheduling
- 👨‍🏫 **Learning Tutor Agent** - Personalized education

### Data (3)
- 🔄 **Data Pipeline Orchestrator** - ETL workflows
- 📑 **Document Processing Agent** - Classification and extraction
- ⚙️ **Workflow Automation Agent** - Process automation

### Healthcare (2)
- 🏥 **Medical Triage Agent** - Symptom assessment
- 🧠 **Mental Health Support Agent** - 24/7 emotional support

### Security (2)
- 🛡️ **Security Incident Response Agent** - Threat monitoring
- ✅ **Compliance Audit Agent** - Multi-framework scanning

### Planning (1)
- 🎯 **Strategic Planning Agent** - Scenario planning and OKRs

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- OpenAI API key (or other LLM provider)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd CCTest
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
# OPENAI_API_KEY=your-api-key-here
```

### Running the Application

**Start the Streamlit app:**
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

**Alternative:** You can also enter your API key directly in the web interface sidebar.

## 📖 Usage

1. **Select an Agent** from the sidebar by category
2. **Configure API Key** in the sidebar if not set via environment
3. **Start Chatting** with the selected agent
4. **Use Features**:
   - 🗑️ Clear Chat - Reset the conversation
   - 🔄 New Session - Start a new session with fresh state

## 🏗️ Architecture

### Project Structure
```
CCTest/
├── app.py                          # Main Streamlit application
├── agents/
│   ├── agent_catalog.py           # Agent registry and metadata
│   ├── business/                  # Business agents
│   │   ├── customer_support_agent.py
│   │   ├── sales_qualification_agent.py
│   │   └── contract_review_agent.py
│   ├── development/               # Development agents
│   ├── research/                  # Research agents
│   ├── content/                   # Content agents
│   ├── data/                      # Data agents
│   ├── healthcare/                # Healthcare agents
│   ├── security/                  # Security agents
│   ├── planning/                  # Planning agents
│   └── README.md                  # Detailed agent documentation
├── .streamlit/
│   └── config.toml                # Streamlit configuration
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

### Technology Stack

- **LangGraph** - Agent orchestration framework
- **LangChain** - LLM application framework
- **Streamlit** - Web interface
- **OpenAI GPT-4** - Language model (configurable)

## 🔧 Configuration

### Environment Variables

Create a `.env` file or set these environment variables:

```bash
# Required
OPENAI_API_KEY=your-openai-api-key

# Optional - LangSmith (monitoring)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-api-key
LANGCHAIN_PROJECT=langgraph-agents
```

### Streamlit Configuration

Edit `.streamlit/config.toml` to customize the UI theme and server settings.

## 💡 Examples

### Using Customer Support Agent
1. Select "Customer Support Agent" from Business category
2. Ask: "I need help tracking my order #12345"
3. The agent will search order history and provide status

### Using Code Review Agent
1. Select "Code Review Agent" from Development category
2. Share code or describe a PR
3. Get security analysis, quality feedback, and suggestions

### Using Market Research Agent
1. Select "Market Research Agent" from Research category
2. Ask: "Analyze the CRM software market"
3. Get competitor analysis, trends, and market sizing

## 🛠️ Development

### Running Tests
```bash
pytest agents/
```

### Code Formatting
```bash
black .
ruff check .
```

### Adding a New Agent

1. Create agent file in appropriate category directory
2. Follow the existing agent structure
3. Add agent metadata to `agents/agent_catalog.py`
4. Update the `load_agent_creator()` function in `app.py`

## 📚 Agent Details

For detailed documentation about each agent, see [agents/README.md](agents/README.md)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

See LICENSE file

## ⚠️ Important Notes

### Healthcare Agents Disclaimer

The Medical Triage and Mental Health Support agents are **NOT** replacements for professional medical or mental health care. They provide informational support only.

- **Medical Triage Agent**: Not medical advice. Always consult healthcare professionals.
- **Mental Health Support Agent**: Not therapy. Crisis resources: Call 988 (Suicide & Crisis Lifeline)

### Production Deployment

For production use:

1. Replace mock tools with real integrations
2. Use production-grade checkpointer (Postgres/Redis)
3. Add authentication and authorization
4. Implement rate limiting
5. Enable LangSmith monitoring
6. Use environment-based secrets management
7. Add error tracking (Sentry, etc.)

## 🔗 Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://docs.langchain.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangSmith](https://smith.langchain.com/)

## 🐛 Troubleshooting

### "Error loading agent"
- Ensure all dependencies are installed
- Check that the agent file exists
- Verify Python path includes the agents directory

### "API Key not configured"
- Set OPENAI_API_KEY in .env file, or
- Enter API key in the sidebar

### "Module not found"
- Run `pip install -r requirements.txt`
- Ensure virtual environment is activated

## 💬 Support

For issues or questions:
- Create a GitHub issue
- Visit [LangChain Forum](https://forum.langchain.com/)

---

**Built with ❤️ using LangGraph and Streamlit**
