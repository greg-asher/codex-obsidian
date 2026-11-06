# codex-obsidian

`codex-obsidian` is a Codex plugin for local Obsidian workflows through the official desktop `obsidian` CLI.

It currently ships seven focused skills:

- `obsidian-official-cli` for core note/metadata workflows, Obsidian Markdown authoring, and reviewed section revisions.
- `obsidian-cli-bases-and-bookmarks` for Bases discovery/query and bookmark workflows.
- `obsidian-cli-runtime-admin` for plugin/theme/snippet and command/hotkey runtime administration.
- `obsidian-cli-devtools` for runtime diagnostics and developer-command workflows.
- `obsidian-cli-sync-and-publish` for Sync workflows and capability-gated Publish workflows with explicit side-effect guardrails.
- `obsidian-cli-workspace-and-navigation` for vault/workspace/tab/navigation and utility workflows.
- `obsidian-cli-workflows` for cited vault answers, explained related notes, project handoffs, and named workflows with preview/apply controls.

## What This Plugin Does

- Reads and inspects local Obsidian vault content through the official desktop CLI.
- Handles note, link, task, property, template, history, Bases, Bookmarks, Sync, developer-command, and workspace/navigation workflows that the documented CLI supports, with Publish handled only when detected as available in the local CLI.
- Exposes named one-command workflow IDs (for example `tasks.rollup`, `daily.bootstrap`, `workspace.focus_mode`) with preview/apply controls.
- Handles runtime administration for plugins, themes, snippets, and command/hotkey surfaces through documented CLI commands.
- Uses minimal local filesystem support only when that is needed to safely support an official CLI workflow.

## Skill Routing Quick Guide

- Use `obsidian-official-cli` for note content and knowledge workflows.
- Use `obsidian-cli-bases-and-bookmarks` for Bases and bookmark query/creation workflows.
- Use `obsidian-cli-runtime-admin` for runtime configuration and command registry workflows.
- Use `obsidian-cli-devtools` for runtime diagnostics, screenshots, and explicit eval/CDP workflows.
- Use `obsidian-cli-sync-and-publish` for Sync state and remote-side-effect operations, and for Publish only when publish commands are available.
- Use `obsidian-cli-workspace-and-navigation` for vault/workspace/tab/navigation operations and utility commands.
- Use `obsidian-cli-workflows` for cited multi-note retrieval or named orchestration across domain skills.

See the detailed matrix and chaining recipes in:

- `skills/obsidian-official-cli/references/obsidian-cli-skill-routing-matrix-2026-04-21.md`

## One-Command Workflow Entry Point

Use explicit workflow command IDs through `obsidian-cli-workflows`:

- `workflow_id=tasks.rollup mode=preview output=json`
- `workflow_id=daily.bootstrap mode=preview vault=Work`
- `workflow_id=workspace.focus_mode mode=preview`
- `workflow_id=workspace.focus_mode mode=apply` (run only after preview + explicit confirmation)

## Cited Vault Answers and Handoffs

Select **Obsidian CLI Workflows** in Codex (installed skill ID `codex-obsidian:obsidian-cli-workflows`) and ask, for example:

- In Work under Projects/Atlas, what did we decide about authentication? Cite the notes and flag conflicting evidence and open questions.
- Find notes related to Projects/Atlas/Decision.md in Work. Explain each match with an excerpt.
- Prepare an Atlas handoff from Work, excluding Projects/Atlas/Private. Preview saving it to Handoffs/Atlas.md.

Results are inline and read-only by default. Search, tag checks, and one-hop links provide bounded coverage. Each material claim is tied to a note path and heading or line when available. Save previews show the exact destination, content and collision policy before apply. Bounded retrieval uses the bundled launcher with Python 3.9+ or an equivalent bounded runner. See the [retrieval playbook](skills/obsidian-cli-workflows/references/cited-retrieval.md) for inputs and limits.

## Capture a Project Decision

Select **Obsidian CLI Workflows** and ask “Preview capturing the decision ‘Use scoped tokens’ for Projects/Atlas.md in Work. Put it in Decisions with the rationale ‘Reduce exposure if a token leaks.’” The decision recipe previews the exact note and project link. After approval, it creates the note once and verifies the result. An identical existing note counts as already present. See the [decision recipe](skills/obsidian-cli-workflows/references/decision-capture.md) for required inputs and the Python 3.9+ renderer.

## Controlled Note Authoring

Invoke `$obsidian-official-cli`, for example: “Update the Risks section of Projects/Atlas.md in Work using these findings.” The skill resolves both vault and exact path, reads current content, previews a minimal diff, rechecks before apply, and verifies the result. It preserves unrelated content and inspects state before retrying a timeout. Existing-file creation defaults to a collision; overwrite requires a reviewed, approved write. Workflow note outputs reuse the same contract.

Obsidian Desktop 1.15 adds native insertion under headings in notes and daily notes. The skill checks the installed command's help for `heading=`, resolves the heading in the approved note, and verifies the placement and line breaks. [Obsidian 1.15 release notes](https://obsidian.md/changelog/2026-11-02-desktop-v1.15.0/)

Section revision has no assumed native patch command. It uses a reviewed exact-text candidate and capability-verified whole-file CLI overwrite only when lossless transport is established and approved. Rechecks are optimistic with a remaining concurrency race. Unsupported patches return the proposed diff and a specific blocker.

Prerequisites: official Obsidian desktop installer 1.12.7+ with CLI enabled/registered and app available. Optional bundled helpers require Python 3.9+ (standard library only). They handle JSON arguments and exact-text previews; they do not install services, configure vaults, or write note content directly. Resolve helper paths from the installed skill, including cached copies. See [authoring/revision details](skills/obsidian-official-cli/references/authoring-and-revision.md) and [validation evidence/remaining live checks](skills/obsidian-official-cli/references/validation.md).

All seven skills retain explicit invocation. Cited retrieval and project decision capture accept plain language after selecting the workflow skill. Other named orchestration uses `workflow_id=`.

## What This Plugin Does Not Do

- It does not target community Obsidian CLIs or plugin-specific APIs.
- It does not cover `obsidian://` launcher automation or Headless Sync workflows.
- It does not bundle MCP servers or connector apps in this version.

## Repository Layout

This repository is the plugin root.

```text
.
├── .codex-plugin/plugin.json
├── .agents/plugins/marketplace.json
├── assets/
└── skills/
```

The source of truth is the unpacked plugin content in this repository. There is no separate packaged copy.

## macOS Zsh Path Override

The Codex Desktop launcher uses `/usr/local/bin/zsh` by default for backward compatibility. If Zsh is installed elsewhere, set `CODEX_OBSIDIAN_ZSH_PATH` to an absolute path before starting Codex. For example:

```bash
export CODEX_OBSIDIAN_ZSH_PATH=/bin/zsh
```

The launcher quotes the resolved path and continues to use the existing sanitized `script + zsh -ilc` execution form.

## Local Install And Test Flow

1. Clone this repository locally.
2. Review `.agents/plugins/marketplace.json`. It exposes this repo as a local marketplace entry with `source.path` set to `./`.
3. Restart Codex so it reloads the repo marketplace metadata.
4. Open the plugin directory in Codex, choose `LumiCorp's Marketplace`, and install `codex-obsidian`.
5. Invoke one skill explicitly and run a small read-only task first to confirm install and routing boundaries.

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
