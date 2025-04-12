# Agents Demo

A multi-agent system that demonstrates the power of AI agents working together to extract and process information from web pages. This project showcases how specialized AI agents can collaborate to perform complex tasks like web scraping, address extraction, and geocoding. Developed using Google ADK and MCP Platform.

## Overview

This project implements a team of specialized AI agents that work together to:
1. Crawl web pages and extract their content
2. Identify and parse addresses from the content
3. Convert addresses into geographic coordinates
4. Present the results in a structured format

The system uses Google's ADK (Agent Development Kit) and MCP (Multi-Component Platform) to create a robust pipeline for information extraction and processing. Each agent in the system has a specific role:

- **Crawler Agent**: Fetches and cleans webpage content using BeautifulSoup4
- **Address Agent**: Identifies and extracts structured address information from text
- **Geocoding Agent**: Converts addresses into precise geographic coordinates
- **Manager Agent**: Orchestrates the workflow between all agents

## Project Structure

```
.
├── src/
│   ├── agents/          # Core agent implementation
│   │   ├── agent.py     # Main agent logic and coordination
│   │   └── config.yaml  # Agent configurations and instructions
│   └── mcp_server/      # MCP server implementation
├── assets/              # Static assets
├── .env                 # Environment variables
└── pyproject.toml       # Project dependencies
```

## How It Works

The system follows a sophisticated workflow:

1. **Web Content Extraction**: The crawler agent fetches webpage content and cleans it for processing
2. **Address Identification**: The address agent analyzes the content to find and structure address information
3. **Geocoding**: Each identified address is converted into precise latitude and longitude coordinates
4. **Result Compilation**: The manager agent combines all information into a structured JSON output

The agents communicate through a well-defined protocol, ensuring reliable data flow and error handling throughout the process.

## Prerequisites

- Python 3.12 or higher
- Poetry for dependency management
- Google API key for LLM Calls

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/agents-demo.git
cd agents-demo
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your Google API key for geocoding services

## Usage

The system can be used to extract and geocode addresses from any webpage. Here's a basic example:

```python
from src.agents.agent import main
import asyncio

# Run the agent system
asyncio.run(main(config, query, user_id, session_id))
```

The output will be a JSON file containing all extracted addresses with their corresponding geographic coordinates.

## Development

This project uses:
- Poetry for dependency management
- MCP for multi-component platform integration
- Google ADK for agent development
- BeautifulSoup4 for web scraping
- LiteLLM for language model interactions
- JSON Repair for data handling

## Technical Details

The system is built with scalability and reliability in mind:
- Each agent operates independently with clear responsibilities
- Error handling and logging are implemented throughout
- The system can process multiple addresses in parallel
- Results are cached and stored in a structured format
