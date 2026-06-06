import os

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".private", ".env"))
mcp = FastMCP("Warlock")

PROFILE_BASE_URI = "profile://"
RESOURCE_BASE_URI = "resource://"


def profile_uri(name: str) -> str:
    return f"{PROFILE_BASE_URI}{{username}}/{name}"


def resource_uri(name: str) -> str:
    return f"{RESOURCE_BASE_URI}{name}"
