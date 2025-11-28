import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")

async def call_tool(latitude: float, longitude: float):
    async with client:
        result = await client.call_tool("get_weather", {"input": {"latitude": latitude, "longitude": longitude}})
        print(result)

asyncio.run(call_tool(-23.55, -46.63))