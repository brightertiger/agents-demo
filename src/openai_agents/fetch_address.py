import asyncio
import os
import shutil
import subprocess
import time
from openai import OpenAI
from typing import Any
from agents import Agent, Runner, gen_trace_id, trace
from agents import set_default_openai_client, set_default_openai_api
from agents.mcp import MCPServerStdio
from mcp.client.stdio import StdioServerParameters
from dotenv import load_dotenv

load_dotenv("../../.env")


def set_llm_model(model_name: str = "gpt-4o-mini"):
    openai_client = OpenAI(model=model_name, api_key=os.getenv("OPENAI_API_KEY"))
    set_default_openai_client(openai_client)
    set_default_openai_api("chat_completitions")
    return openai_client


def set_mcp_server(mcp_server: str = "../mcp_server/mcp_server.py"):
    command = f"python"
    args = [mcp_server]
    env = {"PYTHONUTF8": "1"}
    mcp_server_parameters = StdioServerParameters(command=command, args=args, env=env)
    return mcp_server_parameters


crawling_instructions = """
    You are a web crawler agent.
    You are given a url and you need to crawl the web and return the text address.
    You need to return the text address in the format of a json object with the key "address".
"""

formatting_instructions = """
    You need to return the text address in the format of a json object with the key "address".
"""

geocoding_instructions = """
    You are a geocoding agent.
    You are given a text address and you need to return the latitude and longitude of the address.
    You need to return the latitude and longitude in the format of a json object with the keys "latitude" and "longitude".
"""


async def main(url: str):
    async with MCPServerStdio(params=set_mcp_server(), cache_tools_list=True) as server:
        crawler_agent = Agent(
            name="web_crawler_agent",
            instructions="A crawler agent that crawls a url and returns the text address",
            mcp_servers=[server],
            verbose=True,
        )
