# warlock-agents

Core SDK for context-aware LLM agents. Features dynamic multi-layered markdown profile injection, structured JSON intent parsing, and extensible tool-calling interfaces for workflow automation.

---

## Key Features

- **Layered Persona & Profile Resolver:** Merges public base definitions with gitignored private user constraints and system lore at runtime.
- **Dynamic Skill loading:** Automatically registers and exposes skills from the `.skills/` directory.
- **Multiple Transports:** Supports standard Model Context Protocol (MCP) standard input/output (`stdio`) and streaming HTTP (`streamable-http`) transport modes.
- **Secure Synchronization:** Built-in Tailscale SSH sync tool to securely copy local gitignored assets between development devices.

---

## Project Structure

The repository is organized to cleanly separate core public code/resources from operator-specific private data:

```
warlock-agents/
├── .private/               # Gitignored local configuration and private profiles
│   ├── .env                # Local API tokens, credentials, and YouTrack settings
│   ├── agents/             # Private agent overlays (e.g. Scrum Master torque_overlay.md)
│   └── profiles/           # Operator alignment profiles and sensitive personal lore
├── .public/                # Tracked public assets and base definitions
│   ├── agents/             # Public base agent definitions (e.g. torque.md)
│   └── profiles/           # Public resumes and non-sensitive technical profiles
├── .skills/                # Dynamic custom capabilities/skills loaded by the server
├── .scripts/               # Utility scripts (e.g., private configuration sync script)
├── src/
│   └── warlock/            # Core Python package code (main, tools, resources, core)
└── pyproject.toml          # Package configuration and dependencies
```

---

## Getting Started

### 1. Installation & Environment Setup
Install the project dependencies using `uv`:

```bash
uv sync
```

### 2. Private Configuration Setup
The repository segregates public definitions from operator-specific private credentials and profiles. To initialize your local environment:

1. Copy the gitignored configuration template:
   ```bash
   cp -r .private.template .private
   ```
2. Open `.private/.env` and update your YouTrack domains and credential values.
3. Configure your personal alignment constraints and cognitive rules in `.private/profiles/warlock_profile.md` and `.private/profiles/warlock_lore.md`.

### 3. Running the MCP Server

The Warlock MCP server can be run in two transport modes:

#### Standard I/O Mode (Default)
Ideal for local clients running on the same machine:
```bash
.venv/bin/python -m warlock.main --transport stdio
```

#### Streamable HTTP Mode
Ideal for network/remote access (e.g., exposing the server on a workstation to a laptop client over a Tailscale mesh network). This mode disables DNS rebinding checks to allow traffic routing over private IP ranges:
```bash
.venv/bin/python -m warlock.main --transport streamable-http --host 0.0.0.0 --port 8000
```
*Note: Your client should connect to `http://<server-ip>:8000/mcp`.*

---

## Private Configuration Syncing

To sync your gitignored `.private/` folder securely between devices over a Tailscale network:

1. Enable Tailscale SSH on both environments:
   ```bash
   tailscale up --ssh
   ```
2. Run the sync utility to push local changes to a remote host:
   ```bash
   .scripts/sync-private-configs.sh <remote-tailscale-ip>
   ```
3. To pull changes from a remote host instead:
   ```bash
   .scripts/sync-private-configs.sh --direction pull <remote-tailscale-ip>
   ```

> **SSH Config Requirement:** The sync script uses your local username by default. If your remote username differs (e.g., `warlock-admin` on the Alienware vs. `raworre` on the MSI), add an entry to `~/.ssh/config` on your local machine to avoid authentication failures:
> ```
> Host warlock-alien <tailscale-ip>
>     User warlock-admin
> ```

---

## Orchestrator Session Setup

Subagent type registrations are **ephemeral** — they do not persist across `agy` CLI sessions. At the start of each new orchestrator session, named subagents (`torque`, `clutch`) must be re-registered before they can be invoked.

### Why This Matters
Subagents registered **without** `enable_mcp_tools: true` cannot call `call_mcp_tool` and will not have access to the lazy-loaded `warlock-mcp` YouTrack tools. Without this flag, a subagent will fall back to reading the Python source in `src/warlock/tools/` and executing it directly — bypassing the MCP boundary entirely.

### Registration Protocol
When invoking a named subagent for the first time in a session, the orchestrator must:

1. Fetch the merged persona from the MCP server:
   ```
   read_resource: agent://torque
   ```
2. Register the subagent type via `define_subagent` with `enable_mcp_tools: true`
3. Only then invoke via `invoke_subagent` with the registered type name

This protocol is enforced as a workspace rule in `.agents/AGENTS.md` (Section 3).

