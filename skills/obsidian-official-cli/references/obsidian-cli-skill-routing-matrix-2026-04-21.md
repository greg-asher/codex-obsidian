# Obsidian CLI Skill Routing Matrix (2026-04-21)

Use this matrix to pick the right skill and chain them safely.

## Skill ownership

- `obsidian-official-cli`:
  - note CRUD, search, links, tasks, properties, templates, daily notes, history/diff
- `obsidian-cli-bases-and-bookmarks`:
  - base discovery/query/create workflows and bookmark listing/creation
- `obsidian-cli-runtime-admin`:
  - plugins, restricted mode, themes, snippets, command IDs, hotkeys, command execution
- `obsidian-cli-devtools`:
  - runtime diagnostics: errors, console, DOM/CSS, screenshots, `eval`, `dev:cdp`
- `obsidian-cli-sync-and-publish`:
  - Sync status/history/restore flows and capability-gated Publish flows
- `obsidian-cli-workspace-and-navigation`:
  - vault/workspace/tab/navigation and utility workflows

## Routing examples

- "Append this to Projects/Plan.md" -> `obsidian-official-cli`
- "Query Projects.base Roadmap in JSON and bookmark blocked items" -> `obsidian-cli-bases-and-bookmarks`
- "Install Dataview and enable it" -> `obsidian-cli-runtime-admin`
- "Show console errors from my plugin" -> `obsidian-cli-devtools`
- "Check sync status and, if publish commands are supported, publish changed files" -> `obsidian-cli-sync-and-publish`
- "Load the Daily Review workspace, inspect recents, then open a note in a new tab" -> `obsidian-cli-workspace-and-navigation`

## Chaining patterns

### Plugin debugging chain

1. `obsidian-cli-runtime-admin`: `plugin:reload id=<plugin-id>`
2. `obsidian-cli-devtools`: `dev:errors` and `dev:console`
3. `obsidian-cli-devtools`: `dev:dom` or `dev:css`
4. `obsidian-cli-devtools`: `dev:screenshot`

### Release chain

1. `obsidian-official-cli`: `diff` and `history` on target notes
2. `obsidian-cli-sync-and-publish`: `sync:status` plus publish capability probe (`help publish:status`)
3. if publish is supported: run `publish:status` and `publish:add path=...` or `publish:add changed`
4. if publish is supported: run `publish:list` for verification; otherwise stop with unsupported publish blocker

### Bases research chain

1. `obsidian-cli-bases-and-bookmarks`: `bases` and `base:views`
2. `obsidian-cli-bases-and-bookmarks`: `base:query ... format=json`
3. `obsidian-cli-bases-and-bookmarks`: `bookmark search=...` or `bookmark file=...`
4. `obsidian-official-cli`: targeted `read path=...` follow-up on resulting files

### Runtime customization chain

1. `obsidian-cli-runtime-admin`: read-only inventory (`plugins`, `themes`, `snippets`)
2. `obsidian-cli-runtime-admin`: apply runtime change (`theme:set`, `snippet:enable`, `plugin:enable`)
3. `obsidian-cli-devtools`: verify UI/runtime effect (`dev:dom`, `dev:css`, `dev:errors`)

### Workspace context setup -> note workflow handoff

1. `obsidian-cli-workspace-and-navigation`: `workspace:load name=...` and `tabs`/`recents`
2. `obsidian-cli-workspace-and-navigation`: `open path=... newtab` for intended work context
3. `obsidian-official-cli`: run note-content workflow (`read`, `append`, `tasks`, `properties`)

### Navigation sampling -> targeted core note operations

1. `obsidian-cli-workspace-and-navigation`: `random:read folder=...` or inspect `recents`
2. `obsidian-cli-workspace-and-navigation`: resolve and open selected note target
3. `obsidian-official-cli`: apply targeted edits/analysis with exact `path=` safety

## Guardrail summary

- Keep note-content edits in `obsidian-official-cli` with exact-path mutation rules.
- Keep base and bookmark workflows in `obsidian-cli-bases-and-bookmarks`.
- Keep remote-side-effect Sync operations and capability-gated Publish operations in `obsidian-cli-sync-and-publish`.
- Keep runtime diagnostics and code execution (`eval`, `dev:cdp`) in `obsidian-cli-devtools`.
- Keep runtime admin and customization operations in `obsidian-cli-runtime-admin`.
- Keep vault/workspace/tab/navigation and utility operations in `obsidian-cli-workspace-and-navigation`.
