from . import (
    resources,  # noqa: F401
    tools,  # noqa: F401
)
from .core import mcp

if __name__ == "__main__":
    mcp.run(transport="stdio")
