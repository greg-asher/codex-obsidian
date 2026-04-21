---
name: obsidian-cli-sync-and-publish
description: Use this skill when the user needs official desktop Obsidian CLI Sync or Publish workflows, including status checks, history inspection, restore operations, and publish add/remove flows. This skill is for remote-side-effect operations and must use explicit intent and conservative safety checks.
---

# Obsidian CLI Sync and Publish

Use this skill for Obsidian Sync and Obsidian Publish operations through official desktop `obsidian` CLI commands.

## Routing contract

Use this skill when:
- the user asks for Sync state, Sync history, or Sync restore operations
- the user asks for Publish status, publish add/remove, or publish site checks
- the task is a release/checkpoint flow that depends on Sync or Publish surfaces

Do not use this skill when:
- the request is regular note CRUD, task/property updates, or graph cleanup
- the request is Obsidian Headless automation without desktop app
- the request is community tooling or non-official publish/sync surfaces

## Preconditions

Assume these must be true before relying on this skill:
- `obsidian` command is installed and registered
- Obsidian desktop app is available locally
- Sync and/or Publish are configured in the target vault
- in Codex Desktop on macOS, direct launches can crash; prefer sanitized wrapper

## Codex-safe launcher

In Codex Desktop on macOS, prefer this wrapper:

```bash
script -q /dev/null /usr/local/bin/zsh -ilc 'unset __CFBundleIdentifier LaunchInstanceID XPC_SERVICE_NAME CODEX_CI CODEX_SANDBOX CODEX_SHELL; export TERM=xterm-256color; obsidian ...'
```

Escalate the wrapped command only when required by sandbox boundaries.

## Core operating policy

1. Use only official desktop Sync and Publish CLI commands.
2. For mixed read/write flows, run status checks first (`sync:status`, `publish:status`).
3. Treat mutating commands as high-impact operations.
4. Do not run mutating commands on implicit active-file targets unless the user explicitly requested active-file behavior.
5. For restore operations (`sync:restore`), require explicit `version=<n>` plus explicit `file=` or `path=` unless the user clearly specifies active-file restore.
6. For publish operations, clearly state whether action targets one file, path, or all changed files.
7. Summarize remote side effects before executing mutating operations.
8. If Sync or Publish is not configured, report that blocker and stop.
9. If the request is actually headless/server Sync, say this skill does not cover Headless Sync and stop.

## Risk levels

- low: `sync:status`, `sync:history`, `sync:read`, `sync:deleted`, `publish:site`, `publish:list`, `publish:status`
- medium: `sync`, `sync:open`, `publish:open`
- high: `sync:restore`, `publish:add`, `publish:remove`

## Response contract

Always return:
- command capability used
- risk level (`low`, `medium`, `high`)
- execution mode (`direct` or `escalated`)
- exact command(s) run or proposed
- affected file/path scope
- remote side effects summary (if any)
- blocking reason, if any

## Command families

Sync:
- `sync`
- `sync:status`
- `sync:history`
- `sync:read`
- `sync:restore`
- `sync:open`
- `sync:deleted`

Publish:
- `publish:site`
- `publish:list`
- `publish:status`
- `publish:add`
- `publish:remove`
- `publish:open`

## References

- `references/obsidian-cli-sync-publish-playbook.md`
- `references/limitations-and-boundaries.md`
- `references/validation.md`
- `references/source-links.md`
