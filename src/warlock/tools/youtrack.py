import os

import httpx
from ..core import mcp


@mcp.tool()
async def create_youtrack_issue(
    summary: str,
    description: str,
    tags: list[str] = None,
    priority: str = "Normal",
) -> str:
    """
    Creates a new issue in YouTrack with optional tags and priority.
    Resolves tag names to IDs automatically.
    """
    base_url = os.getenv("YOUTRACK_URL")
    token = os.getenv("YOUTRACK_TOKEN")
    headers = {"Authorization": f"Bearer {token}"}

    resolved_tags = []
    if tags:
        async with httpx.AsyncClient() as client:
            # Fetch all tags to map names to IDs
            tags_resp = await client.get(f"{base_url}/api/tags?fields=id,name", headers=headers)
            if tags_resp.is_success:
                all_tags = tags_resp.json()
                for tag_name in tags:
                    # Try to match name exactly or with a leading #cd
                    match = next(
                        (
                            t
                            for t in all_tags
                            if t["name"].lower() == tag_name.lower()
                               or t["name"].lower() == f"#{tag_name.lower()}"
                        ),
                        None,
                    )
                    if match:
                        resolved_tags.append({"id": match["id"]})

    create_issue_url = f"{base_url}/api/issues?fields=idReadable"

    payload = {
        "project": {"shortName": os.getenv("YOUTRACK_PROJECT_KEY")},
        "summary": summary,
        "description": description,
        "customFields": [
            {"name": "Priority", "$type": "SingleEnumIssueCustomField", "value": {"name": priority}}
        ],
    }

    if resolved_tags:
        payload["tags"] = resolved_tags

    async with httpx.AsyncClient() as client:
        resp = await client.post(create_issue_url, json=payload, headers=headers)

        if resp.is_success:
            data = resp.json()
            issue_id = data["idReadable"]
            issue_url = f"{base_url}/issues/{issue_id}"
            return f"Created new issue: [{issue_id}] - {issue_url}"
        else:
            return f"Failed to create issue: {resp.status_code} - {resp.text}"


@mcp.tool()
async def find_youtrack_issue(
    issue_id: str,
) -> str:
    """
    Search YouTrack for an issue based on the given ID.
    """
    return f"Not implemented: {issue_id}"
