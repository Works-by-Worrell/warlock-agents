import argparse

from . import resources, tools
from .core import mcp
from .resources.skills import load_dynamic_skills_tools

# Prevent Ruff from stripping registration side effects
_ = (resources, tools)

# Execute tool discovery before binding transport
load_dynamic_skills_tools()


def main():
    parser = argparse.ArgumentParser("Warlock MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport protocol to use (default: stdio)", )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host address to bind to when running SSE (default: 0.0.0.0)", )
    parser.add_argument(
        "--port",
        default=8000,
        help="Port to bind to when running SSE (default: 8000)", )

    args = parser.parse_args()

    if args.transport == "stdio":
        print(f"Starting Warlock MCP Server in SSE Mode on http://{args.host}:{args.port}")
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
