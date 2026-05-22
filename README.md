# Multi-Agent Researcher

An intelligent multi-agent system that automates research by searching the web, analyzing content, and generating professional reports with critical feedback.

## Overview

This project orchestrates multiple AI agents to conduct comprehensive research on any topic:

1. **Search Agent** - Finds recent and reliable information using web search
2. **Reader Agent** - Scrapes and extracts detailed content from relevant URLs
3. **Writer Agent** - Synthesizes research into a structured, professional report
4. **Critic Agent** - Reviews and evaluates the report with constructive feedback

## Features

- 🔍 **Automated Web Research** - Real-time information retrieval using Tavily search API
- 📄 **Content Extraction** - Intelligent web scraping with automatic cleanup of irrelevant content
- ✍️ **Report Generation** - AI-powered report writing with structured formatting
- 🔬 **Quality Review** - Automatic critique and scoring of generated reports
- 🔄 **Modular Pipeline** - Seamless agent coordination with state management
- 💾 **Complete Output** - Returns search results, scraped content, report, and feedback

## Architecture

```
Pipeline Flow:
Input Topic
    ↓
[Search Agent] → Web Search Results
    ↓
[Reader Agent] → Scraped Content
    ↓
[Writer Agent] → Professional Report
    ↓
[Critic Agent] → Feedback & Score
    ↓
Output (Complete Research State)
```

## Prerequisites

- Python 3.8+
- Google Gemini API key
- Tavily API key

## Installation

1. **Clone or navigate to the project directory**:

```bash
cd Multi-Agent-researcher
```

2. **Create a virtual environment** (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
   Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_google_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

## Usage

Run the research pipeline with a topic of your choice:

```bash
python pipeline.py
```

You'll be prompted to enter a research topic:

```
Enter a research topic: [Your topic here]
```

### Example Output

The pipeline returns a dictionary containing:

- `search_results` - Web search findings with titles, URLs, and snippets
- `scraped_content` - Detailed content extracted from the most relevant source
- `report` - Full research report with introduction, findings, conclusion, and sources
- `feedback` - Critic evaluation with score and improvement suggestions

## Project Structure

```
Multi-Agent-researcher/
├── agents.py          # Agent and chain definitions
├── pipeline.py        # Main research orchestration pipeline
├── tools.py           # Web search and scraping tools
├── requirements.txt   # Project dependencies
└── README.md         # This file
```

## File Descriptions

### `agents.py`

Defines the AI agents and processing chains:

- **Search Agent**: Uses `web_search` tool to find information
- **Reader Agent**: Uses `scrape_url` tool for detailed content
- **Writer Chain**: Synthesizes research into reports
- **Critic Chain**: Evaluates and scores reports

### `pipeline.py`

Orchestrates the multi-step research process:

- Executes agents in sequence
- Manages state across steps
- Combines results for report generation
- Collects feedback

### `tools.py`

Implements core research tools:

- **web_search()**: Searches using Tavily API (max 2 results)
- **scrape_url()**: Extracts clean text content from URLs

## Configuration

### Model Settings (agents.py)

- **Model**: Gemini 2.5 Flash
- **Temperature**: 1.0 (creative responses)
- **Max Retries**: 2

### Search Settings (tools.py)

- **Max Search Results**: 2 per query
- **Scrape Limit**: 3000 characters per URL
- **Timeout**: 10 seconds per request

## API Keys Required

1. **Google Gemini API**
   - Sign up at https://makersuite.google.com/app/apikey
   - Required for LLM operations

2. **Tavily Search API**
   - Sign up at https://tavily.com
   - Required for web search functionality

## Dependencies

Key packages used:

- `langchain` - Agent and chain orchestration
- `langchain-google-genai` - Google Gemini integration
- `tavily-python` - Web search API
- `beautifulsoup4` - Web scraping
- `requests` - HTTP requests
- `python-dotenv` - Environment variable management
- `rich` - Pretty console output

See `requirements.txt` for complete list and versions.

## Example Workflow

```python
from pipeline import run_research_pipeline

# Run research on a topic
results = run_research_pipeline("Artificial Intelligence in Healthcare")

# Access results
print("Search Results:", results["search_results"])
print("Report:", results["report"])
print("Feedback:", results["feedback"])
```

## Tips for Best Results

- **Specific Topics**: Use specific, well-defined research topics for better results
- **Technical Terms**: Include relevant keywords to guide the search
- **Follow-up Research**: Use feedback to refine and re-run on related topics
- **API Quotas**: Monitor your API usage (especially Tavily search limits)

## Troubleshooting

**"Could not scrape URL" error**

- The website may have blocked automated access
- Try a different URL from search results
- Check your internet connection

**API Key errors**

- Verify `.env` file exists and contains correct keys
- Ensure API keys are active and have remaining quota
- Check for spaces or formatting issues in keys

