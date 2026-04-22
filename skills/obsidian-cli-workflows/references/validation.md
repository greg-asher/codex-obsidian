# Validation

## Structural checks

1. Confirm skill files exist:
   - `SKILL.md`
   - `agents/openai.yaml`
   - `assets/eval-prompts.csv`
   - `references/workflow-registry.md`
   - `references/playbook.md`
   - `references/limitations-and-boundaries.md`
   - `references/validation.md`
   - `references/source-links.md`
2. Confirm frontmatter `name` is unique and set to `obsidian-cli-workflows`.
3. Confirm `allow_implicit_invocation: false` in `agents/openai.yaml`.

## Registry checks

1. Confirm registry command IDs match the full 18-command set exactly:
   - `daily.bootstrap`
   - `daily.review`
   - `inbox.capture`
   - `project.kickoff`
   - `project.status_digest`
   - `tasks.rollup`
   - `tasks.close_and_log`
   - `research.pack`
   - `graph.repair_plan`
   - `graph.orphan_reduction`
   - `base.snapshot`
   - `base.intake_create`
   - `bookmark.curate`
   - `workspace.focus_mode`
   - `recents.triage`
   - `runtime.debug_snapshot`
   - `sync.health_check`
   - `publish.release_gate`
2. Confirm each entry defines intent, required/optional inputs, chained steps with owning skill, default output, risk, and apply guardrails.

## Behavior checks

1. Preview mode returns:
   - step plan
   - target summary
   - risk classification
2. Apply mode enforces explicit confirmation semantics for medium/high workflows.
3. Ambiguous targets fail closed.
4. `publish.release_gate` always probes `help publish:status` before `publish:*` actions.
5. Unsupported publish capability path returns blocker and no `publish:*` execution.

## Cross-skill boundary checks

1. Workflow skill remains orchestration-only.
2. Domain skills remain direct command owners.
3. Runtime-admin/devtools/sync-publish ownership remains unchanged.
4. Workspace/navigation direct command ownership remains in `obsidian-cli-workspace-and-navigation`.
