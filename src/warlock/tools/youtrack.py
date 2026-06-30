import logging
import os

import httpx

from ..core import mcp

logger = logging.getLogger(__name__)


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

    logger.info("Writing new YouTrack issue")

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
async def search_youtrack_issues(query: str, max_results: int = 10) -> str:
    """
    Search YouTrack for issues matching the query.

    Supports standard YouTrack search query syntax, including:
    - Unresolved tickets: "#Unresolved"
    - Board and Sprint specific lists: "Board {Board Name}: {Sprint Name}"
        (e.g., "Board Warlock MCP: Sprint.001")
    - Specific tags: "tag: #Warlock"
    """
    base_url = os.getenv("YOUTRACK_URL")
    token = os.getenv("YOUTRACK_TOKEN")
    headers = {"Authorization": f"Bearer {token}"}

    params = {
        "query": query,
        "$top": max_results,
        "fields": "idReadable,summary,customFields(name,value(name))",
    }

    logger.info(f"Searching YouTrack issues: {query}")

    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{base_url}/api/issues", params=params, headers=headers)

        if not resp.is_success:
            return f"Failed to search issues: {resp.status_code} - {resp.text}"
        else:
            issues = resp.json()

            if not issues:
                return f"No issues found for query: {query}"

            content = [f"## Search Results - {query}\n"]
            for issue in issues[:max_results]:
                stage_field = next(
                    (f for f in issue.get("customFields", []) if f["name"] == "Stage"),
                    None,
                )
                status = (
                    stage_field["value"]["name"]
                    if stage_field and stage_field.get("value")
                    else "Unknown"
                )
                content.append(f"- **{issue['idReadable']}**: {issue['summary']} [{status}]")
            return "\n".join(content)


@mcp.tool()
async def get_youtrack_issue_details(issue_id: str) -> str:
    """
    Fetch details about a given YouTrack issue.
    """
    base_url = os.getenv("YOUTRACK_URL")
    token = os.getenv("YOUTRACK_TOKEN")
    headers = {"Authorization": f"Bearer {token}"}

    params = {"fields": "idReadable,summary,description,tags(name),customFields(name,value(name))"}

    logger.info(f"Fetching details for YouTrack issue: {issue_id}")

    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{base_url}/api/issues/{issue_id}", params=params, headers=headers)

        if not resp.is_success:
            return f"Failed to fetch details: {resp.status_code} - {resp.text}"
        else:
            issue = resp.json()

            if not issue:
                return f"Failed to find issue: {issue_id}"

            stage_field = next(
                (f for f in issue.get("customFields", []) if f["name"] == "Stage"),
                None,
            )
            status = (
                stage_field["value"]["name"]
                if stage_field and stage_field.get("value")
                else "Unknown"
            )
            tags_list = issue.get("tags") or []
            tags_str = ", ".join(f"#{tag['name']}" for tag in tags_list) or "None"

            content = [
                f"# {issue['idReadable']} - {issue['summary']}\n",
                f"- **Status**: {status}\n",
                f"- **Tags**: {tags_str}\n",
                f"- **Description**:\n{issue.get('description', 'No description provided.')}",
            ]

            return "\n".join(content)
