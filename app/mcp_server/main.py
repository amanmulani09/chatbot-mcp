from app.mcp_server.research_server import mcp

if __name__ == "__main__":
    mcp.run(transport='stdio')