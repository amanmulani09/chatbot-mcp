from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# create server parameters for stdio conenctions 

server_params = StdioServerParameters(
    command="uv",
    args=["run","research_server.py"],
    env=None
)

async def run():
    async with stdio_client(server_params) as (read,write):
        async with ClientSession(read,write) as session:
            
            # initilise the 1:1 session with the mcp server 
            await session.initialize()
            
            # list all available tools 
            tools = session.list_tools()
            
            # call a tool ; this will be a process query method 
            result = session.call_tool('tool-name',arguments=)