# codex-obsidian

`codex-obsidian` is a Codex plugin for local Obsidian workflows through the official desktop `obsidian` CLI.

It currently ships one skill, `obsidian-official-cli`, which is intentionally narrow: it focuses on documented desktop CLI note and metadata operations, preserves exact-path mutation safety, and stays out of community tooling, plugin APIs, and non-desktop Obsidian surfaces.

## What This Plugin Does

- Reads and inspects local Obsidian vault content through the official desktop CLI.
- Handles note, link, task, property, template, and history workflows that the documented CLI supports.
- Uses minimal local filesystem support only when that is needed to safely support an official CLI workflow.

## What This Plugin Does Not Do

- It does not target community Obsidian CLIs or plugin-specific APIs.
- It does not cover `obsidian://` launcher automation, Publish, or Headless Sync workflows.
- It does not bundle MCP servers or connector apps in this version.

## Repository Layout

This repository is the plugin root.

```text
.
├── .codex-plugin/plugin.json
├── .agents/plugins/marketplace.json
├── assets/
└── skills/obsidian-official-cli/
```

The source of truth is the unpacked plugin content in this repository. There is no separate packaged copy.

## Local Install And Test Flow

1. Clone this repository locally.
2. Review `.agents/plugins/marketplace.json`. It exposes this repo as a local marketplace entry with `source.path` set to `./`.
3. Restart Codex so it reloads the repo marketplace metadata.
4. Open the plugin directory in Codex, choose the `Codex Obsidian Local` marketplace, and install `codex-obsidian`.
5. Invoke `obsidian-official-cli` explicitly and run a small read-only task first to confirm the install and skill boundary.

Codex installs local plugins from a cached copy. After you change the plugin, restart Codex and reinstall or refresh from the repo marketplace flow so the installed copy picks up the new files.

## Publish Status

This repository is prepared to be shared on GitHub as a single public plugin repo.

OpenAI's current Codex plugin docs still describe official public plugin publishing as "coming soon," so this repo is structured for:

- GitHub distribution
- local marketplace installs
- future official directory publication when self-serve publishing is available

## Suggested GitHub Metadata

- Description: `Codex plugin for local Obsidian workflows through the official desktop CLI.`
- Topics: `codex-plugin`, `obsidian`, `obsidian-cli`, `agent-skill`, `openai-codex`

## Notes For Future Publish Prep

- GitHub repo: `https://github.com/greg-asher/codex-obsidian`
- Add an install-surface screenshot under `assets/` after the plugin has been verified through the local marketplace flow.
