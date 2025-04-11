import requests
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Web Tool Server")

@mcp.tool(
    name="crawl_to_markdown",
    description="Crawl a web page and convert it to markdown", 
)
def crawl_to_markdown(url: str) -> str:
    """Crawl a web page and convert it to markdown"""
    response = requests.get(url)
    response.raise_for_status()  # Raise exception for HTTP errors
    soup = BeautifulSoup(response.text, 'html.parser')
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text


@mcp.tool(
        name="geocode_address", 
        description="Convert an address to geographic coordinates"
)
def geocode_address(address: str) -> dict:
    """Convert an address to geographic coordinates"""
    endpoint = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "MCP-GeocodingService/1.0"  # Required by Nominatim
    }
    response = requests.get(endpoint, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
    if not data:
        return {"error": "Address not found"}
    result = data[0]
    return {
        "latitude": float(result["lat"]),
        "longitude": float(result["lon"]),
        "display_name": result["display_name"]
    }

if __name__ == "__main__":
    # mcp.run(transport="sse")
    mcp.run(transport="stdio")