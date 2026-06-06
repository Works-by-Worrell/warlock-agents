# Public Profiles (`.public/`)

This directory contains the public-facing technical profiles for operators of the Warlock Engine.

Unlike the `.private/` folder, this directory is tracked by version control. It serves as the open-source resume,
professional experience, and capability matrix that can be shared publicly.

---

## 1. What Belongs Here

* **`{username}.md`**: The public technical and professional profile for a specific operator (e.g., `warlock.md`). It
  documents:
    * Core technical stack (JVM/Java, C#, Python, TypeScript).
    * Professional experience, past roles, and leadership history.
    * Operational philosophies (e.g., "Meat, Fire, Butter, and Salt").
    * Hardware and development environment stats.

---

## 2. Technical Integration

The FastMCP server ([resources.py](file:///home/raworre/Source/WBW/warlock-agents/resources.py)) serves these profiles
through parameterized routes:

* `profile://{username}/public` dynamically loads and returns the contents of `.public/{username}.md`.
* `profile://{username}/combined` merges this public profile with the corresponding private profile from `.private/`.

---

## 3. The Rules of the Boundary

1. **Zero Secrets:** Because this directory is committed to source control, **never** place API tokens, credentials,
   private contact info, or sensitive personal lore in here. Keep those behind the airlock in `.private/`.
2. **Accuracy and Authority:** Keep these profiles up-to-date. This is the foundation the agent uses to evaluate if a
   public open-source issue matches your engineering experience.
