# Public Assets (`.public/`)

This directory contains public-facing technical configurations and profiles that are committed to version control. Unlike the `.private/` folder, this directory is tracked and shared publicly on git.

---

## Directory Structure

```
.public/
├── agents/             # Public base agent persona definitions (e.g. torque.md)
└── profiles/           # Public resumes and non-sensitive technical profiles (e.g. warlock.md)
```

---

## 1. Key Components

### `agents/`
Contains public base definitions for LLM agent roles and personas (e.g., `torque.md` for the Scrum Master agent). 
* These files specify the core role descriptions, tags, and standard tools exposed to the agent.
* Private extensions to these roles are overlaid from `.private/agents/` at runtime.

### `profiles/`
* **`{username}.md`**: The public technical resume and professional profile for a specific operator (e.g., `warlock.md`). It documents the operator's core stack, experience history, and development environments.
* The Warlock server queries these profiles to matches issues and projects to your real engineering experience.

---

## 2. Technical Integration

The FastMCP server resources resolve public assets dynamically:
* **Profiles:** Served by `src/warlock/resources/profiles.py` via `profile://{username}/public` (and concatenated via `profile://{username}/combined`).
* **Agents:** Served by `src/warlock/resources/agents.py` via `agent://{agent_name}`.

---

## 3. Rules of the Public Boundary

1. **Zero Secrets:** Because this folder is committed to public source control, **never** put API tokens, sensitive IP/contact info, passwords, or private user details here.
2. **Accuracy:** Keep the technical stack and resume up-to-date to ensure the agent has accurate context when matching tickets.
