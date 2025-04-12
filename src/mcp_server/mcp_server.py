import requests
import json
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("Web Tool Server")


@mcp.tool(
    name="crawl_to_markdown",
    description="Crawl a web page and convert it to markdown",
)
def crawl_to_markdown(url: str) -> str:
    """Crawl a web page and convert it to markdown"""
    response = requests.get(url)
    response.raise_for_status()  # Raise exception for HTTP errors
    soup = BeautifulSoup(response.text, "html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = "\n".join(chunk for chunk in chunks if chunk)
    return text


@mcp.tool(
    name="geocode_address",
    description="Convert an address to geographic coordinates using OpenStreetMap",
)
def geocode_address(address: dict) -> dict:
    """Convert an address to geographic coordinates"""
    endpoint = "https://nominatim.openstreetmap.org/search"
    if isinstance(address, str):
        address = json.loads(address)
    address_string = f"{address.get('address', '')}, "
    address_string += f"{address.get('city', '')}, "
    address_string += f"{address.get('state', '')}, "
    address_string += f"{address.get('zip', '')}, "
    address_string += f"{address.get('country', '')}"
    params = {"q": address_string, "format": "json", "limit": 1}
    headers = {"User-Agent": "MCP-GeocodingService/1.0"}  # Required by Nominatim
    response = requests.get(endpoint, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
    if not data:
        return {"latitude": 0.0, "longitude": 0.0}
    result = data[0]
    return {
        "latitude": float(result["lat"]),
        "longitude": float(result["lon"]),
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
