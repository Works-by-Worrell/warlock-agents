#!/usr/bin/env python3
import argparse
import asyncio
import json
import os
import sys

# Resolve the project root (warlock-agents directory)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Self-re-execute using the project's virtual environment if mcp is not available
try:
    import mcp
except ImportError:
    venv_python = os.path.join(PROJECT_ROOT, ".venv", "bin", "python")
    if os.path.exists(venv_python) and sys.executable != venv_python:
        os.execv(venv_python, [venv_python] + sys.argv)
    else:
        print(
            "Error: The 'mcp' library is not installed, and no virtual environment was found at .venv/",
            file=sys.stderr,
        )
        print(
            "Please run this script inside the project's virtual environment or using 'uv run'.",
            file=sys.stderr,
        )
        sys.exit(1)

DEFAULT_AGENTS = ["torque", "broker"]
DEFAULT_FALLBACK_URL = "http://100.112.192.38:8000/mcp"


def get_mcp_server_url() -> str:
    """Reads the Warlock MCP server URL from the workspace configuration."""
    config_path = os.path.abspath(os.path.join(PROJECT_ROOT, "..", ".agents", "mcp_config.json"))
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                url = config.get("mcpServers", {}).get("warlock-mcp", {}).get("serverUrl")
                if url:
                    return url
        except Exception as e:
            print(
                f"⚠️ Warning: Failed to parse workspace mcp_config.json ({e}). Using default fallback URL."
            )
    return DEFAULT_FALLBACK_URL


async def fetch_and_install_agent(server_url: str, agent_name: str) -> bool:
    """Queries the Warlock MCP server for the agent's persona and installs it locally."""
    from mcp import ClientSession
    from mcp.client.streamable_http import streamable_http_client

    print(f"🔍 Fetching agent '{agent_name}' from Warlock MCP server...")

    try:
        async with streamable_http_client(server_url) as (read_stream, write_stream, _):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                resource_uri = f"agent://{agent_name}"
                res = await session.read_resource(resource_uri)

                if not res.contents:
                    print(f"❌ Error: Received empty content from server for agent '{agent_name}'.")
                    return False

                content = res.contents[0]
                if not hasattr(content, "text") or not content.text:
                    print(f"❌ Error: Persona content for '{agent_name}' is not text.")
                    return False

                text_content = content.text
                if text_content.startswith("Error: Agent definition for"):
                    print(f"❌ Server Error: {text_content.strip()}")
                    return False

                # Define destination path in workspace scope
                global_dest_dir = os.path.expanduser(
                    os.path.join("~", ".gemini", "config", "agents", agent_name)
                )
                os.makedirs(global_dest_dir, exist_ok=True)
                workspace_dest_file = os.path.join(global_dest_dir, "agent.md")

                with open(workspace_dest_file, "w", encoding="utf-8") as f:
                    f.write(text_content)

                print(f"  ✅ Installed '{agent_name}' globally to {workspace_dest_file}")
                return True

    except Exception as e:
        print(
            f"❌ Connection Error: Could not retrieve agent '{agent_name}' from Warlock MCP server at {server_url}."
        )
        print(f"   Details: {e}")
        return False


async def async_main():
    parser = argparse.ArgumentParser(
        description="Fetch and install agent personas from the Warlock MCP server dynamically."
    )
    parser.add_argument(
        "agents",
        nargs="*",
        help=f"List of agent names to fetch and install (default: {', '.join(DEFAULT_AGENTS)}).",
    )
    parser.add_argument(
        "--url",
        help="Custom URL for the Warlock MCP server. Defaults to value in workspace mcp_config.json.",
    )

    args = parser.parse_args()

    # Resolve server URL
    server_url = args.url if args.url else get_mcp_server_url()

    # Resolve agents to install
    agents_to_install = args.agents if args.agents else DEFAULT_AGENTS

    success = True
    for agent in agents_to_install:
        result = await fetch_and_install_agent(server_url, agent)
        if not result:
            success = False

    if not success:
        sys.exit(1)


def main():
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(130)


if __name__ == "__main__":
    main()
