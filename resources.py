import os

from core import mcp
from core import profile_uri

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@mcp.resource(profile_uri('public'))
def get_public_profile(username: str) -> str:
    """Returns the public technical profile (ME.md)"""
    public_path = os.path.join(BASE_DIR, ".public", f"{username}.md")

    if not os.path.exists(public_path):
        return f"Error: Public profile {username} not found."

    with open(public_path) as f:
        return f.read()


@mcp.resource(profile_uri('private'))
def get_private_profile(username: str) -> str:
    """
    Safely returns local personal alignment constraints and distilled identity
    lore from the gitignored boundary.
    """
    private_path = os.path.join(BASE_DIR, ".private", f"{username}_alignment.md")
    lore_path = os.path.join(".private", f"{username}_lore.md")

    content = []
    if os.path.exists(private_path):
        with open(private_path) as f:
            content.append("--- PRIVATE USER ALIGNMENT ---\n")
            content.append(f.read())

    if os.path.exists(lore_path):
        with open(lore_path) as f:
            content.append("\n--- PRIVATE USER LORE ---\n")
            content.append(f.read())

    return "\n".join(content) if content else "No private user profile information found"


@mcp.resource(profile_uri('combined'))
def get_combined_profile() -> str:
    public = get_public_profile()
    private = get_private_profile()
    return f"--- PUBLIC PROFILE ---\n{public}\n\n--- PRIVATE PROFILE ---\n{private}\n"
