import os
import httpx
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(".warlock", ".env"))
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

@mcp.tool()
async def create_youtrack_issue(summary: str, description: str) -> str:
    create_issue_url = f"{os.getenv('YOUTRACK_URL')}/api/issues?fields=idReadable"
    payload = {
        "project": { "shortName": os.getenv("YOUTRACK_PROJECT_KEY") },
        "summary": summary,
        "description": description
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(create_issue_url, json=payload, headers={"Authorization": f"Bearer {os.getenv('YOUTRACK_TOKEN')}"})

        if resp.is_success:
            data = resp.json()
            issue_id = data['idReadable']
            issue_url = f"{os.getenv('YOUTRACK_URL')}/issues/{issue_id}"
            return f"Created new issue: [{issue_id}] - {issue_url}"
        else:
            return f"Failed to create issue: {resp.status_code} - {resp.text}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
