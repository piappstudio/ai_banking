import sys
import tools.tool
from app import mcp

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--sse":
        import uvicorn
        print("Starting MCP server with SSE transport on port 4001...")
        uvicorn.run(mcp.sse_app, host="0.0.0.0", port=4001)
    else:
        mcp.run(transport="stdio")
