import os
import logging
import asyncio
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    SseServerParams,
    StdioServerParameters,
)

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
MODEL_GPT_4O = "openai/gpt-4o"


async def get_tools_async(path_to_mcp_server: str):
    logging.info("Attempting to connect to MCP Filesystem server...")
    tools, exit_stack = await MCPToolset.from_server(
        connection_params=StdioServerParameters(
            command="python",  # Command to run the server
            args=[path_to_mcp_server],
        )
    )
    logging.info("MCP Toolset created successfully.")
    return tools, exit_stack


async def main():
    tools, exit_stack = await get_tools_async(
        path_to_mcp_server="./src/mcp_server/mcp_server.py"
    )
    try:
        print(tools)
        return tools
    finally:
        await exit_stack.aclose()


if __name__ == "__main__":
    asyncio.run(main())
