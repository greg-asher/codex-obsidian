# One-Command Workflow Candidate Catalog (2026-04-21)

This catalog lists user-facing "one-command" workflow candidates built from the current `codex-obsidian` skill surface.
These candidates are implemented as named workflow IDs in `obsidian-cli-workflows/references/workflow-registry.md`.

Each candidate is intended to be invoked as one user intent, even though it chains multiple official CLI actions under the hood.

## Candidate Fields

- `id`: stable workflow identifier
- `one_command`: suggested command-style name
- `user_intent`: what the user asks for
- `chain`: representative action sequence
- `skills`: skill surfaces involved
- `risk`: `low` | `medium` | `high`
- `notes`: key constraints or guardrails

## Candidate Catalog

## Daily and Personal Ops

1. `id`: `wf_daily_bootstrap`
- `one_command`: `daily.bootstrap`
- `user_intent`: "Set up my daily note with today’s template, carry-over tasks, and quick metrics."
- `chain`: `daily:path` -> `daily:read` -> `tasks daily` -> `daily:append` -> `wordcount daily note`
- `skills`: `obsidian-official-cli`
- `risk`: `medium`
- `notes`: mutates daily note; requires clear append policy.

2. `id`: `wf_daily_review`
- `one_command`: `daily.review`
- `user_intent`: "Give me a concise end-of-day review from today’s note and tasks."
- `chain`: `daily:read` -> `tasks daily` -> `backlinks daily note` -> structured summary output
- `skills`: `obsidian-official-cli`
- `risk`: `low`
- `notes`: read-only by default.

3. `id`: `wf_inbox_capture`
- `one_command`: `inbox.capture`
- `user_intent`: "Capture this idea in my inbox and tag it correctly."
- `chain`: `unique` or `create` -> `property:set` -> `tags` check -> optional `open newtab`
- `skills`: `obsidian-official-cli`, `obsidian-cli-workspace-and-navigation`
- `risk`: `medium`
- `notes`: requires folder/property defaults.

## Project and Task Management

4. `id`: `wf_project_kickoff_note`
- `one_command`: `project.kickoff`
- `user_intent`: "Create a project kickoff note with metadata, starter tasks, and links."
- `chain`: `create path=... template=...` -> `property:set` -> `append` task block -> `links` verification
- `skills`: `obsidian-official-cli`
- `risk`: `medium`
- `notes`: template presence should be checked first.

5. `id`: `wf_status_digest`
- `one_command`: `project.status_digest`
- `user_intent`: "Generate a status digest for a project folder."
- `chain`: `search path=...` -> `tasks path=... verbose format=json` -> `properties name=status` -> digest note output
- `skills`: `obsidian-official-cli`
- `risk`: `low`
- `notes`: read-heavy; optional write of digest note.

6. `id`: `wf_task_rollup`
- `one_command`: `tasks.rollup`
- `user_intent`: "Roll up open tasks across selected folders with urgency buckets."
- `chain`: `tasks todo verbose format=json` -> `search:context` for blockers -> grouped report
- `skills`: `obsidian-official-cli`
- `risk`: `low`
- `notes`: no mutation needed.

7. `id`: `wf_task_closure_sync`
- `one_command`: `tasks.close_and_log`
- `user_intent`: "Mark this task done and log completion in daily note."
- `chain`: `task ref=... done` -> `daily:append` completion log -> `tasks daily` verify
- `skills`: `obsidian-official-cli`
- `risk`: `medium`
- `notes`: dual-write workflow.

## Knowledge and Graph Intelligence

8. `id`: `wf_research_pack`
- `one_command`: `research.pack`
- `user_intent`: "Build a focused research pack on a topic from my vault."
- `chain`: `search:context query=...` -> `outline` top candidates -> `backlinks` + `links` graph context -> pack note
- `skills`: `obsidian-official-cli`
- `risk`: `low`
- `notes`: can be read-only or write final pack note.

9. `id`: `wf_link_repair_plan`
- `one_command`: `graph.repair_plan`
- `user_intent`: "Find unresolved links and propose repair actions."
- `chain`: `unresolved verbose format=json` -> `search` likely targets -> proposed rename/move map
- `skills`: `obsidian-official-cli`
- `risk`: `low`
- `notes`: planning-only by default; apply mode could be high risk.

10. `id`: `wf_orphan_reduction`
- `one_command`: `graph.orphan_reduction`
- `user_intent`: "Reduce orphan/dead-end notes with actionable suggestions."
- `chain`: `orphans` + `deadends` -> `tags/properties` context -> suggestion report -> optional backlink seed append
- `skills`: `obsidian-official-cli`
- `risk`: `low` (report) / `medium` (apply)
- `notes`: two-mode workflow (report vs apply).

## Bases and Structured Views

11. `id`: `wf_base_view_snapshot`
- `one_command`: `base.snapshot`
- `user_intent`: "Export a base view snapshot for reporting."
- `chain`: `bases` -> `base:views` -> `base:query format=json|csv` -> snapshot note/file
- `skills`: `obsidian-cli-bases-and-bookmarks`
- `risk`: `low`
- `notes`: read-only.

12. `id`: `wf_base_intake_create`
- `one_command`: `base.intake_create`
- `user_intent`: "Create a new tracked item through the correct base view."
- `chain`: `base:views` validate -> `base:create` -> `open/newtab` -> optional metadata patch
- `skills`: `obsidian-cli-bases-and-bookmarks`, `obsidian-cli-workspace-and-navigation`
- `risk`: `high`
- `notes`: direct content mutation; needs strict target confirmation.

13. `id`: `wf_bookmark_curator`
- `one_command`: `bookmark.curate`
- `user_intent`: "Curate bookmarks for active project context."
- `chain`: `bookmarks verbose` -> `bookmark file|search|folder` adds -> post-check listing
- `skills`: `obsidian-cli-bases-and-bookmarks`
- `risk`: `medium`
- `notes`: mutation is reversible but should be explicit.

## Workspace and Runtime Context

14. `id`: `wf_focus_mode_switch`
- `one_command`: `workspace.focus_mode`
- `user_intent`: "Switch to my focus workspace and open priority note set."
- `chain`: `workspace:load` -> `tabs` -> `open path=... newtab` -> `recents` check
- `skills`: `obsidian-cli-workspace-and-navigation`
- `risk`: `high`
- `notes`: layout/state mutation.

15. `id`: `wf_recent_triage`
- `one_command`: `recents.triage`
- `user_intent`: "Triage my recently opened notes into next actions."
- `chain`: `recents` -> `wordcount`/`tasks` on top notes -> triage summary note
- `skills`: `obsidian-cli-workspace-and-navigation`, `obsidian-official-cli`
- `risk`: `low`
- `notes`: read-first with optional summary write.

16. `id`: `wf_plugin_debug_snapshot`
- `one_command`: `runtime.debug_snapshot`
- `user_intent`: "Capture a plugin/runtime debug snapshot."
- `chain`: `plugin:reload` -> `dev:errors` + `dev:console` -> `dev:screenshot path=...` -> report note
- `skills`: `obsidian-cli-runtime-admin`, `obsidian-cli-devtools`, `obsidian-official-cli`
- `risk`: `medium`
- `notes`: avoid `eval` unless explicitly requested.

## Capability-Gated Sync/Publish Ops

17. `id`: `wf_sync_health_check`
- `one_command`: `sync.health_check`
- `user_intent`: "Check sync health and history risks before I continue working."
- `chain`: `sync:status` -> `sync:deleted` -> optional `sync:history` for target files
- `skills`: `obsidian-cli-sync-and-publish`
- `risk`: `low`
- `notes`: fully supported in current verified surface.

18. `id`: `wf_publish_release_gate`
- `one_command`: `publish.release_gate`
- `user_intent`: "Run publish readiness check and execute publish actions if supported."
- `chain`: `help publish:status` capability probe -> if supported then `publish:status` + `publish:list` + `publish:add`
- `skills`: `obsidian-cli-sync-and-publish`
- `risk`: `high`
- `notes`: blocked in current local CLI build where `publish:*` is unavailable.

## Priority-Selection Input Set (for next step)

Use this shortlist when choosing first-priority one-command commands:

- `daily.bootstrap`
- `project.kickoff`
- `tasks.rollup`
- `research.pack`
- `base.snapshot`
- `workspace.focus_mode`
- `runtime.debug_snapshot`
- `sync.health_check`

These were selected for high user value with current verified command support and clear guardrails.

## Proposed Launch Priority (P0/P1/P2)

## P0 (launch first)

- `tasks.rollup`
  - high recurring utility, low mutation risk, clear output surface
- `daily.bootstrap`
  - daily habit workflow with immediate repeat usage
- `research.pack`
  - strong leverage for knowledge retrieval and synthesis
- `sync.health_check`
  - low-risk operational safety check with high trust value

## P1 (launch second)

- `project.kickoff`
  - strong project onboarding value but requires template/default conventions
- `base.snapshot`
  - high value for structured reporting users; lower universal usage
- `recents.triage`
  - useful recovery flow after context switching, mostly read-first

## P2 (launch after core adoption)

- `runtime.debug_snapshot`
  - high value for advanced users; narrower audience
- `workspace.focus_mode`
  - useful but stateful/high-impact layout mutation
- `base.intake_create`
  - high-risk base mutation flow requiring stricter guardrails
- `tasks.close_and_log`
  - useful dual-write flow but not as universal as rollup/bootstrap
- `bookmark.curate`
  - helpful curation flow, generally lower urgency
- `graph.repair_plan`
  - planning-heavy cleanup workflow; lower day-one demand
- `graph.orphan_reduction`
  - medium-term vault quality workflow
- `daily.review`
  - valuable, but often secondary to bootstrap/rollup in early rollout
- `project.status_digest`
  - useful for teams, but less universal than P0 commands
- `inbox.capture`
  - strong utility but overlaps with existing lightweight create flows
- `publish.release_gate`
  - currently capability-gated and blocked in local CLI where `publish:*` is unavailable
