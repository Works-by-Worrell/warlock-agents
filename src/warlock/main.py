from .core import mcp
from .resources.skills import load_dynamic_skills_tools

# Execute tool discovery before binding transport
load_dynamic_skills_tools()

if __name__ == "__main__":
    mcp.run(transport="stdio")
