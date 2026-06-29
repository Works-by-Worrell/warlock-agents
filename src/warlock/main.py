import argparse
import logging
import sys

from . import resources, tools
from .core import mcp
from .resources.skills import load_dynamic_skills_tools

# Configure logging to go strictly to stderr
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr, )
logger = logging.getLogger(__name__)

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
        type=int,
        default=8000,
        help="Port to bind to when running SSE (default: 8000)", )

    args = parser.parse_args()

    if args.transport == "sse":
        logger.info(f"Starting Warlock MCP Server in SSE Mode on http://{args.host}:{args.port}")
        mcp.settings.host = args.host
        mcp.settings.port = int(args.port)
        mcp.run(transport="sse")
    else:
        logger.info("Starting Warlock MCP Server in stdio mode")
        mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
