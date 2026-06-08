import os

from ..core import PROJECT_ROOT, mcp


@mcp.resource("agent://{agent_name}")
def get_agent_persona(agent_name: str) -> str:
    """
    Returns the layered agent persona. Combines the public base definition
    with the gitignored private overlay if it exists locally.
    """
    public_path = os.path.join(PROJECT_ROOT, "agents", f"{agent_name}.md")
    private_path = os.path.join(PROJECT_ROOT, "agents", ".private", f"{agent_name}_overlay.md")

    content = []

    # Load public base agent
    if os.path.exists(public_path):
        with open(public_path) as f:
            content.append(f"## BASE PERSONA ({agent_name})\n")
            content.append(f.read())
    else:
        return f"Error: Public agent definition for '{agent_name}' not found."

    # Private overlay
    if os.path.exists(private_path):
        with open(private_path) as f:
            content.append("\n\n## PRIVATE OPERATIONAL OVERLAY\n")
            content.append(f.read())

    return "\n".join(content)


@mcp.prompt()
def agent_session(
    agent_name: str,
    username: str,
    skills: str = ""
) -> str:
    """
    Assembles a complete agent system prompt containing:
    1. Agent Persona (Personality)
    2. User Profile (Constraints/Lore)
    3. Custom Skills (Abilities)
    """
    persona = get_agent_persona(agent_name)

    from .profiles import get_combined_profile
    user_profile = get_combined_profile(username)

    skills_content = []
    if skills:
        skills_dir = os.path.join(PROJECT_ROOT, "skills")
        for s in [s.strip() for s in skills.split(",") if s.strim()]:
            skill_md_path = os.path.join(skills_dir, s, "SKILL.md")
            if os.path.exists(skill_md_path):
                with open(skill_md_path) as f:
                    skills_content.append(f"### Skill: {s}\n{f.read()}")
            else:
                skills_content.append(f"### Skill: {s}\nError: Skill '{s}' not found.")

    skills_section = "\n\n".join(skills_content) \
        if skills_content else "No specialized skills loaded."

    return f"""You are booting into a specialized agent session.

        =========================================
        1. YOUR PERSONA (IDENTITY & STYLE)
        =========================================
        {persona}

        =========================================
        2. USER PROFILE & CONSTRAINTS
        =========================================
        {user_profile}

        =========================================
        3. ACTIVE SKILLS (ABILITIES)
        =========================================
        {skills_section}

        =========================================
        SESSION INITIALIZATION INSTRUCTIONS
        =========================================
        Initialize your system state using the guidelines above. Adhere strictly to user profile
        constraints.
    """
