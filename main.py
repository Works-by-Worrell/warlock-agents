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
    """Safely retrieves local personal alignment constraints and distilled identity lore from the gitignored boundary."""
    private_path = os.path.join(".warlock", "alignment.md")
    lore_path = os.path.join(".warlock", "IDENTITY_DISTILLED.md")

    content = []
    if os.path.exists(private_path):
        with open(private_path) as f:
            content.append(f.read())

    if os.path.exists(lore_path):
        with open(lore_path) as f:
            content.append("\n--- IDENTITY MANIFESTO ---\n")
            content.append(f.read())

    return "\n".join(content) if content else "No private alignment constraints configured locally."


@mcp.resource("profile://combined")
def get_combined_profile() -> str:
    """Merges public and private layers into a unified context for Warlock-Agents."""
    public = get_public_profile()
    private = get_private_profile()
    return f"{public}\n\n--- PRIVATE ALIGNMENT & LORE ---\n\n{private}"


@mcp.tool()
def evaluate_project_fit(repo_name: str, issue_description: str) -> str:
    """
    Evaluates whether a target open-source repository issue maps effectively to the user's combined profile.
    """
    # Future state: Core prompt orchestration and token cost optimization logic
    return f"Warlock Engine Pipeline Action: Analyzing compatibility matrix for {repo_name}..."

@mcp.tool()
async def create_youtrack_issue(summary: str, description: str, tags: list[str] = None, priority: str = "Normal") -> str:
    """
    Creates a new issue in YouTrack with optional tags and priority.
    Resolves tag names to IDs automatically.
    """
    base_url = os.getenv('YOUTRACK_URL')
    token = os.getenv('YOUTRACK_TOKEN')
    headers = {"Authorization": f"Bearer {token}"}
    
    resolved_tags = []
    if tags:
        async with httpx.AsyncClient() as client:
            # Fetch all tags to map names to IDs
            tags_resp = await client.get(f"{base_url}/api/tags?fields=id,name", headers=headers)
            if tags_resp.is_success:
                all_tags = tags_resp.json()
                for tag_name in tags:
                    # Try to match name exactly or with a leading #
                    match = next((t for t in all_tags if t['name'].lower() == tag_name.lower() or t['name'].lower() == f"#{tag_name.lower()}"), None)
                    if match:
                        resolved_tags.append({"id": match['id']})
    
    create_issue_url = f"{base_url}/api/issues?fields=idReadable"
    
    payload = {
        "project": { "shortName": os.getenv("YOUTRACK_PROJECT_KEY") },
        "summary": summary,
        "description": description,
        "customFields": [
            {
                "name": "Priority",
                "$type": "SingleEnumIssueCustomField",
                "value": { "name": priority }
            }
        ]
    }

    if resolved_tags:
        payload["tags"] = resolved_tags

    async with httpx.AsyncClient() as client:
        resp = await client.post(create_issue_url, json=payload, headers=headers)

        if resp.is_success:
            data = resp.json()
            issue_id = data['idReadable']
            issue_url = f"{base_url}/issues/{issue_id}"
            return f"Created new issue: [{issue_id}] - {issue_url}"
        else:
            return f"Failed to create issue: {resp.status_code} - {resp.text}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
