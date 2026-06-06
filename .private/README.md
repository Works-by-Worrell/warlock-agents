# The Airlock (`.private/`)

This is the gitignored perimeter. It exists to separate public engine code from personal alignment constraints, local
environment variables, and distilled system lore.

Keep the corporate fluff out. This is the structural foundation for keeping the agent aligned with the human driving the
keyboard.

---

## 1. What Belongs Here

* **`.env`**: Local environment variables, API tokens (YouTrack, GitHub), and instance URLs. If it connects to an
  external API, the credentials sit here.
* **`{username}_profile.md`**: The raw, unmasked constraints for a specific operator (e.g., `warlock_profile.md`). What
  conditions do we build under? Who do we work with? (e.g., remote-first, high autonomy, zero defense/military
  projects). Replaces the legacy `alignment.md`.
* **`{username}_lore.md`**: Personal anchors (e.g., `warlock_lore.md`)—DJing (Hrothgar Warlock), bank angling (Trout
  Magnets, Rocky Mountain Arsenal), the Subaru's manual gearbox, and AuDHD baseline constraints. The tactile realities
  that ground the operator when cognitive systems overload. Replaces the legacy `lore.md`.

---

## 2. Technical Integration

The FastMCP server ([resources.py](file:///home/raworre/Source/WBW/warlock-agents/resources.py)) traverses this boundary
using dynamic username parameters to inject local context into the agent's workspace:

* `profile://{username}/private` dynamically loads and concatenates `{username}_profile.md` and `{username}_lore.md`
  from this folder.
* `profile://{username}/combined` merges the public technical profile (from `.public/`) with the private files in this
  folder.

---

## 3. The Rules of the Boundary

1. **Keep it Local:** The top-level [.gitignore](file:///home/raworre/Source/WBW/warlock-agents/.gitignore) uses
   `.private/*` to ensure this directory and all operator-specific profiles/lore never get pushed to remote
   repositories. Protect this boundary.
2. **No Bullshit:** Document constraints cleanly. Keep interfaces explicit, contracts transparent, and code clean. No
   HR-approved spin or academic fluff.
3. **Meat & Salt:** Keep configurations basic, physical, and highly reliable. If a tool doesn't need to exist, don't
   build it.
