import os

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv(dotenv_path=os.path.join(".warlock", ".env"))
mcp = FastMCP("Warlock")

PROFILE_BASE_URI = "profile://"
RESOURCE_BASE_URI = "resource://"


def profile_uri(name: str) -> str:
    return f"{PROFILE_BASE_URI}{name}"


def resource_uri(name: str) -> str:
    return f"{RESOURCE_BASE_URI}{name}"
