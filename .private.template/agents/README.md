# Private Agent Overlays

This folder contains gitignored markdown files containing private operational instructions, guidelines, voice/tone overrides, and credentials for your agents.

At runtime, the dynamic agent resolver (`agent://{agent_name}`) merges the public base definition (`.public/agents/{agent_name}.md`) with the matching file in this folder (`.private/agents/{agent_name}_overlay.md` or `.private/agents/{agent_name}.md`).

## Example Structure
Refer to `torque_overlay.md` in this directory for a reference implementation of a private Scrum Master overlay.
