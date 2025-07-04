# 🔬 Deep Research Agent

A sophisticated multi-agent research system that conducts comprehensive research with intelligent clarification questions, contextual search planning, and professional report generation using OpenAI's Agents framework.

## ✨ Features

### 🎯 Intelligent Clarification System
- Automatically generates 3 targeted clarification questions based on your research query
- Handles partial responses (answer only the questions you want)
- Creates enriched research context for better results

### 🤖 Multi-Agent Architecture
- **Clarifier Agent**: Generates intelligent clarification questions
- **Planner Agent**: Creates targeted search strategies based on clarifications
- **Search Agent**: Performs contextual web searches with enhanced relevance
- **Writer Agent**: Synthesizes findings into comprehensive reports
- **Email Agent**: Delivers beautifully formatted reports via email
- **Research Manager**: Orchestrates all agents with handoff patterns

### 🎨 Modern Interface
- Clean, intuitive Gradio web interface
- Step-by-step workflow visualization
- Real-time progress updates
- Mobile-responsive design

### 📊 Comprehensive Reporting
- Executive summaries with key findings
- Structured sections with detailed analysis (1000+ words)
- Actionable recommendations
- Areas for further research
- Professional markdown formatting
- HTML email delivery with beautiful styling

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- UV package manager (recommended)
- OpenAI API key
- SendGrid API key (for email delivery)

### Installation

1. **Clone or download the project**
   ```bash
   cd /path/to/deep-research
   ```

2. **Install dependencies with UV (recommended)**
   ```bash
   uv sync
   ```
   
   Or install manually:
   ```bash
   pip install openai-agents>=0.0.17 gradio>=5.33.1 python-dotenv>=1.1.0 pydantic>=2.11.5 sendgrid>=6.12.3 certifi>=2025.4.26
   ```

3. **Set up environment variables**
   
   Copy the example environment file and update with your API keys:
   ```bash
   cp env.example .env
   ```
   
   Then edit `.env` with your actual API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   SENDGRID_API_KEY=your_sendgrid_api_key_here
   FROM_EMAIL=your_email@example.com
   TO_EMAIL=your_email@example.com
   ```

4. **Important: API Keys Setup**
   
   You'll need to obtain:
   - **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
   - **SendGrid API Key**: Get from [SendGrid Console](https://app.sendgrid.com/settings/api_keys)
   - **Email Configuration**: Update `FROM_EMAIL` and `TO_EMAIL` in your `.env` file
   
   ⚠️ **Security Note**: Never commit your `.env` file to version control. It contains sensitive API keys.

5. **Run the application**
   ```bash
   python main.py
   ```
   
   Or with UV:
   ```bash
   uv run main.py
   ```

6. **Open your browser**
   The application will automatically open at `http://localhost:7860`

## 🐳 Docker Deployment

For easier deployment and isolation, you can run the application using Docker:

### Method 1: Docker Compose (Recommended)
```bash
# 1. Set up environment variables
cp env.example .env
# Edit .env with your API keys

# 2. Build and run with Docker Compose
docker-compose up --build

# 3. Access the application at http://localhost:7860
```

### Method 2: Docker Build
```bash
# 1. Build the Docker image
docker build -t deep-research .

# 2. Run the container
docker run -p 7860:7860 --env-file .env deep-research
```

### Docker Benefits
- **Isolated Environment**: No conflicts with system Python
- **Easy Deployment**: Works consistently across different systems
- **Production Ready**: Includes health checks and proper user management
- **Scalable**: Easy to deploy to cloud platforms

## 🔄 How It Works

### 1. Query Input
Enter your research query (e.g., "Impact of AI on healthcare industry")

### 2. Clarification Questions
The system generates 3 intelligent questions to refine your research:
- **Scope**: What specific aspects to focus on
- **Audience**: Who the research is for
- **Context**: Timeline, geography, or other constraints

### 3. Enhanced Research
Based on your clarifications, the system:
- Plans targeted searches using the Planner Agent
- Executes multiple concurrent searches via the Search Agent
- Analyzes results with context awareness

### 4. Report Generation
The Writer Agent creates a comprehensive report with:
- Executive summary
- Detailed sections (1000+ words)
- Key findings and recommendations
- Areas for further research

### 5. Email Delivery
The Email Agent sends a beautifully formatted HTML email with the complete report

## 💡 Usage Examples

### Basic Research
```
Query: "Future of renewable energy"
→ Get clarification questions
→ Provide answers or skip
→ Receive comprehensive report
```

### Quick Research
```
Query: "Latest AI developments"
→ Answer clarification questions
→ Get targeted research
```

### Clarification Examples

**Query**: "Marketing strategies for startups"

**Clarification Questions**:
1. What industry or market segment should I focus on?
2. What's your target company size (early-stage, growth-stage)?
3. Are you looking for digital marketing, traditional marketing, or both?

**Your Response**:
```
1. SaaS and tech startups
2. Early-stage with limited budget
3. Primarily digital marketing with focus on content and social media
```

## 🏗️ Architecture

### Agent Workflow
```
User Query → Clarifier Agent → Research Manager
                ↓
Research Context → Planner Agent → Search Plan
                ↓
Search Agent (parallel searches) → Search Results
                ↓
Writer Agent → Report Generation → Email Agent
```

### Key Components

- **`clarifier_agent.py`**: Intelligent question generation using OpenAI Agents
- **`planner_agent.py`**: Context-aware search planning (3 targeted searches)
- **`search_agent.py`**: Enhanced web search with WebSearchTool
- **`writer_agent.py`**: Comprehensive report synthesis (gpt-4o-mini)
- **`email_agent.py`**: Professional email formatting with SendGrid
- **`research_manager.py`**: Multi-agent orchestration with Runner
- **`deep_research.py`**: Gradio web interface
- **`main.py`**: Application entry point with environment checking

### Technical Framework
- Built on **OpenAI Agents** framework with Agent Runner
- Uses **function_tool** decorators for agent communication
- Implements **trace** functionality for debugging
- Includes fallback workflow for reliability
- All agents use **gpt-4o-mini** for cost efficiency

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | ✅ | OpenAI API key for AI agents |
| `SENDGRID_API_KEY` | ✅ | SendGrid API key for email delivery |
| `FROM_EMAIL` | ✅ | Sender email address for reports |
| `TO_EMAIL` | ✅ | Recipient email address for reports |

### Email Configuration

Email addresses are now configurable through environment variables in your `.env` file:

```env
FROM_EMAIL=your_email@example.com   # Sender email address
TO_EMAIL=your_email@example.com     # Recipient email address
```

**Note**: Both email addresses can be the same if you want to send reports to yourself.

### Customization

You can customize the system by modifying:

- **Search Strategy**: Edit `planner_agent.py` to change search planning logic (currently 3 searches)
- **Report Structure**: Modify `writer_agent.py` to adjust report format and length
- **UI Layout**: Update `deep_research.py` to change interface design
- **Email Templates**: Customize `email_agent.py` for different email styles
- **Agent Models**: Change model settings in individual agent files

## 🛠️ Development

### Project Structure
```
deep-research/
├── pyproject.toml         # UV project configuration with dependencies
├── uv.lock               # UV lock file
├── main.py               # Application entry point
├── deep_research.py      # Gradio web interface
├── research_manager.py   # Multi-agent orchestrator with Runner
├── clarifier_agent.py    # Clarification questions (3 questions)
├── planner_agent.py      # Search planning (3 searches)
├── search_agent.py       # Web search execution with WebSearchTool
├── writer_agent.py       # Report generation (1000+ words)
├── email_agent.py        # Email delivery with SendGrid
└── README.md            # This file
```

### Adding New Agents

1. Create new agent file following the pattern:
   ```python
   from agents import Agent
   
   agent = Agent(
       name="YourAgent",
       instructions="Your instructions here",
       model="gpt-4o-mini",
       # Add tools, output_type as needed
   )
   ```

2. Import and integrate in `research_manager.py`
3. Add function_tool wrapper if needed
4. Update workflow in `run_research_workflow()`
5. Update UI in `deep_research.py` if needed

### Dependencies

Key dependencies from `pyproject.toml`:
- `openai-agents>=0.0.17` - Core agent framework
- `gradio>=5.33.1` - Web interface
- `python-dotenv>=1.1.0` - Environment variables
- `pydantic>=2.11.5` - Data validation
- `sendgrid>=6.12.3` - Email delivery
- `certifi>=2025.4.26` - SSL certificates

### Testing

The system includes error handling and fallback mechanisms:
- Mock search results when APIs are unavailable
- Fallback workflow when manager agent fails
- Graceful degradation for missing services
- Comprehensive error logging

Run development tools:
```bash
# Linting
uv run ruff check

# Formatting  
uv run black .

# Type checking
uv run mypy .

# Tests (if you add them)
uv run pytest
```

## 🔧 Troubleshooting

### Common Issues

1. **"Missing required environment variables"**
   - Create `.env` file with `OPENAI_API_KEY` and `SENDGRID_API_KEY`
   - Ensure no extra spaces or quotes around values

2. **"Failed to send email"**
   - Verify SendGrid API key is valid
   - Update hardcoded email addresses in `email_agent.py`
   - Ensure SendGrid account is properly configured

3. **"Search failed"**
   - Check OpenAI API key is valid and has credits
   - Verify internet connection
   - Check OpenAI Agents framework is properly installed

4. **Interface won't start**
   - Ensure port 7860 is available
   - Try changing port in `main.py`
   - Check for conflicting Python environments
   - Run `uv sync` to ensure dependencies are installed

5. **Agent execution fails**
   - Check OpenAI API quotas and limits
   - Verify `openai-agents` package version (>=0.0.17)
   - Check trace logs for detailed error information

### Debug Mode

Enable debug logging by adding to your code:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

View execution traces at: `https://platform.openai.com/traces/trace?trace_id={trace_id}`

## 📈 Performance

### Optimization Features

- **Concurrent Searches**: System runs 3 searches in parallel via Search Agent
- **Efficient Models**: Uses `gpt-4o-mini` for cost-effective processing
- **Fallbacks**: Graceful degradation when services are unavailable
- **Agent Framework**: Optimized with OpenAI Agents Runner for performance

### Scaling Considerations

For production deployment:
- Use async/await throughout (already implemented)
- Add Redis for session management
- Implement proper logging and monitoring
- Add rate limiting for API calls
- Use environment-specific configurations
- Consider agent caching strategies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following the existing agent patterns
4. Test thoroughly with the development tools
5. Submit a pull request

## 📄 License

This project is for educational purposes. Please ensure you comply with all API terms of service when using OpenAI and SendGrid APIs.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review error messages and trace logs
3. Verify your environment variables and email configuration
4. Test with simple queries first
5. Check OpenAI API quotas and SendGrid configuration

---

**Built with ❤️ using OpenAI Agents, Gradio, and UV Package Manager**