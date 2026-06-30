# The Airlock (`.private/`)

This is the gitignored perimeter. It separates public engine code and base configurations from personal alignment constraints, local environment variables, credentials, and distilled system lore.

Keep all user-specific context and API tokens out of public tracking. This directory is fully ignored by git (`.private/*` in `.gitignore`).

---

## Directory Structure

```
.private/
├── .env                # Local API tokens, YouTrack credentials, and URLs
├── agents/             # Private agent overlays (e.g. torque_overlay.md)
└── profiles/           # Personal user alignment profiles and lore
```

---

## 1. Key Components

### `.env`
Holds local environment variables, third-party API tokens (e.g., YouTrack, GitHub), and instance URLs. Any external credential used by your tools sits strictly in this file.

### `agents/`
Contains private operational overlays for AI personas (e.g., `{agent_name}_overlay.md` or `{agent_name}.md`). 
* For example, the `torque_overlay.md` scrum master overlay specifies custom instructions/personality traits that overlay the base `torque.md` definition without exposing them to public commits.

### `profiles/`
* **`{username}_profile.md`**: Custom alignment constraints for the operator (e.g., `warlock_profile.md`). Defines operating boundaries, tasking requirements, and focus criteria.
* **`{username}_lore.md`**: Tactile personal grounding facts and context (e.g., `warlock_lore.md`). Grounds the operator and agent in real-world anchors when cognitive systems overload.

---

## 2. Technical Integration

The server traversing code reads this boundary to dynamically construct prompts:
* **Environment Variables:** Loaded via `src/warlock/core.py` from `.private/.env` on server startup.
* **User Profiles:** Resolved in `src/warlock/resources/profiles.py` using parameterized routes (`profile://{username}/private` and `profile://{username}/combined`).
* **Agent Personas:** Resolved in `src/warlock/resources/agents.py` (`agent://{agent_name}`), merging public base personas with any private overlay found here.

---

## 3. Rules of the Airlock

1. **Protect the Boundary:** Never stage or force-commit files in this folder.
2. **Sync Securely:** Use `.scripts/sync-private-configs.sh` to copy this folder between local devices over Tailscale SSH. Never sync it via git.
3. **No HR Fluff:** Document real, physical constraints. Keep instruction sets transparent and simple.
