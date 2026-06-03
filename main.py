import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Warlock")

@mcp.resource("profile://public")
def get_public_profile() -> str:
    """Retrieves the public technical profile (ME.md)"""
    with open("ME.md") as f:
        return f.read()


@mcp.resource("profile://private")
def get_private_profile() -> str:
    """Safely retrieves local personal alignment constraints from the gitignored boundary."""
    private_path = os.path.join(".warlock", "alignment.md")
    if os.path.exists(private_path):
        with open(private_path) as f:
            return f.read()
    return "No private alignment constraints configured locally."


@mcp.tool()
def evaluate_project_fit(repo_name: str, issue_description: str) -> str:
    """
    Evaluates whether a target open-source repository issue maps effectively to the user's combined profile.
    """
    # Future state: Core prompt orchestration and token cost optimization logic
    return f"Warlock Engine Pipeline Action: Analyzing compatibility matrix for {repo_name}..."


if __name__ == "__main__":
    mcp.run(transport="stdio")
