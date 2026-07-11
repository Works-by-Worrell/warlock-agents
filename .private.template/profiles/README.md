# Private User Profiles & Lore

This folder stores gitignored Markdown files detailing the user's specific context, personal preferences, behavioral constraints, and background lore.

The dynamic resolver merges the public profiles (`.public/profiles/{username}.md`) with the matching files in this folder to construct the user context injected into every agent session:
1. **`{username}_profile.md`:** Alignment constraints, coding directives, and target work environments (e.g., `operator_profile.md`).
2. **`{username}_lore.md`:** Sensitive personal background, history, and neurodevelopmental guidelines (e.g., `operator_lore.md`).
