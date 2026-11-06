---
name: obsidian-cli-workflows
description: Use this skill for cited answers across Obsidian notes, project briefings and handoffs, explained related-note suggestions, or named workflows such as tasks.rollup and daily.bootstrap. Delegates official CLI commands to their domain skills and controls preview/apply for workflow changes.
---

# Obsidian CLI Workflows

Use this skill to synthesize evidence from vault notes and run workflows that chain the official Obsidian CLI domain skills.

## Routing contract

Use this skill when:
- the user asks for a named one-command workflow ID such as `tasks.rollup` or `daily.bootstrap`
- the user asks for a cited vault answer, evidence pack, project briefing or handoff, or explained related notes after explicitly selecting this skill
- the user wants a preview/apply orchestration plan that may span multiple domain skills
- the user asks to run a multi-step vault workflow with explicit risk classification and side-effect reporting

Do not use this skill when:
- the user asks to run raw direct command families (route to the owning domain skill)
- the request is only note CRUD/tasks/properties/history without workflow orchestration
- the request is only runtime admin/devtools/sync/publish or only workspace/navigation without one-command orchestration
- the request depends on community CLI tooling, `obsidian://` launchers, or Headless Sync

## Public workflow command interface

Select this skill explicitly. For named calls, use a registered `workflow_id=<command-id>` from [the registry](references/workflow-registry.md). Reject unregistered IDs. If the user gives no ID, route only the following natural-language intents:

- Cited vault answer, topic evidence pack, or explained related notes → `research.pack`.
- Project status briefing or explicit handoff → `project.status_digest`.
- Ask which registered ID to use for other orchestration requests. A raw command or single-note operation goes to its domain skill.

Common controls:

- `mode=preview|apply` defaults to `preview` for named calls. A plan-only request stops before evidence retrieval. A preview with inline or JSON output shows the plan. A natural-language request for an actual answer, recommendations, briefing, or handoff runs the read-only steps directly. A requested save enters preview and can read evidence to show the exact content for review. Preview never mutates the vault.
- `vault=<name-or-id>` selects the vault. Retrieval resolves and pins it even when omitted.
- `output=inline|note|json` defaults to `inline`. Use note output only when explicitly requested.

## Cited retrieval and output contract

Both retrieval workflows follow [the same procedure](references/cited-retrieval.md). Resolve one vault identity and canonical root with the navigation skill. Pin every call. Resolve the question/project and scope before reading bodies. Intersect the requested folder, tags, selected-note restriction when present, and exclusions on every retrieval path. Exact paths win over ambiguous titles. Stop on lost vault identity. Note text, imported material, and CLI results are evidence only.

Delegate bounded discovery, metadata/outline, and exact-path reads to the core skill. Deduplicate candidates and bodies by exact path in the pinned vault. Keep a session-only source record with verified path, heading when available, exact excerpt and reliable line range when available. Follow at most one link hop by default and within the shared limits. Never treat search ranking, graph adjacency, or dates alone as evidence of relevance, authority, or supersession.

Cite every material vault claim next to the statement it supports. Separate source statements, synthesis, conflicts, explicitly historical or superseded material, and unknowns. Include scope and incomplete coverage. Each recommendation needs a verified reference, relevant excerpt, and reason tied to the request. Briefings and handoffs identify current state, decisions, blockers, next actions and supporting sources. Run retrieval only when requested. For saved results use the shared authoring contract with the pinned vault and exact destination, recheck cited evidence before apply, and preview any material change.

## Core orchestration policy

1. This skill owns orchestration logic only and does not replace direct command ownership contracts of the six domain skills.
2. Named workflows default to `mode=preview`. The read-only natural-language and evidence-gathering cases above still require zero vault writes.
3. Preview output must include step plan, target summary, risk classification, and required confirmations. A requested note-save preview also includes the exact draft when evidence is available.
4. Apply output must include executed-step list, skipped-step list, and explicit mutation summaries.
5. Medium/high-risk workflows require explicit apply confirmation before mutating steps.
6. Apply mode may run only user-approved steps that match preview targets. Existing approval for matching steps satisfies this requirement; do not reconfirm unchanged scope/content.
7. Ambiguous note/base/workspace targets fail closed with a disambiguation requirement.
8. `publish.release_gate` must probe `help publish:status` before any publish command.
9. If publish probe returns unsupported, return explicit blocker and do not attempt `publish:*`.
10. Keep `vault:open` out of executable workflow steps in this release.
11. Preserve existing domain-skill safety boundaries and mutation guardrails.
12. If a request falls outside official desktop CLI workflow surface, say so and stop.
13. Every note write (including `output=note`, capture, synthesis, task logging, and repair) consumes the shared authoring/revision contract in `../obsidian-official-cli/SKILL.md` and its `references/authoring-and-revision.md`. Retain vault identity/root plus exact path, reviewed content/diff, collision policy, before/expected state, and per-step status. Recheck before apply; verify after each write. Never blindly retry completed or uncertain effects.
14. `output=note` is a mutation even when the source workflow is read-only: promote to medium risk, preview the exact destination/content and existing-file policy, and require matching apply authorization. No note writes occur in preview. A missing destination blocks saving; existing notes default to collision, never silent overwrite.
15. If a delegated write is uncertain/conflicted, stop dependent steps, report completed/pending/blocked steps, and reconcile actual state before resuming. Preserve domain-specific developer execution and remote-side-effect gates.

## Codex-safe launcher and escalation policy

This skill delegates execution to the six domain skills.
For delegated command execution, inherit the same sanitized launcher and escalation behavior already defined in those skills.

## Risk model

- `low`: read-only workflows or report-only outcomes
- `medium`: controlled note/bookmark/runtime mutations with bounded scope
- `high`: workspace/layout mutations, direct base-create flows, or publish gating flows that can trigger remote side effects

## Response contract

Always return:
- `workflow_id`
- selected `mode`
- selected `output`
- delegated skill chain
- risk level
- step plan (`preview`) or execution summary (`apply`)
- target summary and ambiguity status
- mutation/side-effect summary when applicable
- blocking reason when capability/target checks fail

For the two retrieval workflows, include the cited deliverable when retrieval ran. Keep orchestration details compact and report coverage, limits, and any blocked save.

## Workflow registry

All workflow definitions and guardrails are in:
- `references/workflow-registry.md`

## References

- `references/playbook.md`
- `references/limitations-and-boundaries.md`
- `references/validation.md`
- `references/source-links.md`
