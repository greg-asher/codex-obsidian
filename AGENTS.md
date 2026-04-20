# Repository guidance

## Scope

- This repository is the source of truth for the `codex-obsidian` plugin.
- Treat repo root as the plugin root.
- Keep the repository publishable as a single-plugin GitHub repo.

## Layout

- Keep the plugin manifest at `.codex-plugin/plugin.json`.
- Keep bundled skills under `skills/<skill-name>/`.
- Keep presentation assets under `assets/`.
- Keep repo marketplace metadata at `.agents/plugins/marketplace.json` for local install verification.

## Authoring expectations

- Keep the plugin focused on local Obsidian workflows through the official desktop `obsidian` CLI.
- Keep each skill narrow, explicit, and easy to reason about.
- Put routing rules, operating rules, and output contracts in `SKILL.md`.
- Keep skill-specific references, validation notes, and eval assets adjacent to the skill.
- Preserve existing safety boundaries unless the official Obsidian CLI surface actually changes.

## Maintenance

- Prefer root-level guidance only for rules that affect the whole plugin.
- If a correction is specific to `obsidian-official-cli`, update that skill directly.
- Do not reintroduce unrelated scratch or multi-plugin repository content here.
