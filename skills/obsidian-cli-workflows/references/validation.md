# Validation

## Structural checks

1. Confirm skill files exist:
   - `SKILL.md`
   - `agents/openai.yaml`
   - `assets/eval-prompts.csv`
   - `references/workflow-registry.md`
   - `references/playbook.md`
   - `references/cited-retrieval.md`
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

## Representative apply matrix

1. Low-risk checks:
   - `workflow_id=tasks.rollup mode=apply`
   - `workflow_id=sync.health_check mode=apply`
   - confirm no unintended mutation side effects are reported or executed
2. Medium-risk checks:
   - `workflow_id=daily.bootstrap mode=apply`
   - `workflow_id=runtime.debug_snapshot mode=apply`
   - confirm explicit apply confirmation + mutation summaries before execution
3. High-risk checks:
   - `workflow_id=workspace.focus_mode mode=apply`
   - `workflow_id=base.intake_create mode=apply`
   - confirm explicit apply confirmation, strict target matching, and fail-closed behavior on ambiguity

## Cross-skill boundary checks

1. Workflow skill remains orchestration-only.
2. Domain skills remain direct command owners.
3. Runtime-admin/devtools/sync-publish ownership remains unchanged.
4. Workspace/navigation direct command ownership remains in `obsidian-cli-workspace-and-navigation`.

## Cited retrieval fixture

Copy [Cited Retrieval Fixture](../assets/fixtures/Cited%20Retrieval%20Fixture/) to a temporary location and open the copy as a separate Obsidian vault. Keep the copy outside any synced personal vault. Use the explicit skill and run cases 025–035 from [the evaluation prompts](../assets/eval-prompts.csv). To test a successful save, prepare a `Handoffs` folder in the copy, review the exact destination/draft, approve it, and compare both the selected vault and a second disposable vault to their before-state. Use this expected evidence:

| Scenario | Expected result |
| --- | --- |
| Authentication answer | Cite `Atlas/Decision.md § Decision` for employee OIDC and continued API service tokens. `Atlas/Rollout.md § Implementation` confirms staging success and the production security-review blocker. `Atlas/Archive/Auth Proposal.md § Status` records supersession. `Atlas/Support.md` still describes password sign-in in a draft. Use lines to distinguish its repeated headings and avoid claiming the draft was deployed. |
| Open question and recommendations | `Atlas/Risks – João's notes.md § Identity provider outage` supports the emergency-access gap. For a Decision anchor, recommend Rollout for implementation evidence and the old proposal for decision history, with excerpts and verified edges. Report the missing signoff only if encountered within the depth limit. |
| Scope and safety | Resolve the duplicate `Decision.md` before reading a user-provided title. Both tags exclude Catering. Folder excludes Borealis. `Atlas/Private` excludes Payroll even via backlinks and allows `Atlas/PrivateNotes/Café.md`. The imported block in João's note supplies no execution authority. |
| Partial evidence | With `max_notes=1`, disclose unread candidates. For truncated capture, unsupported metadata, empty search, and unresolved links, check that the result distinguishes each and avoids unsupported citations. |
| Handoff and save | Cite the blocker, Ana's review action, and the still-open emergency-access design. Snapshot both vaults before preview. Check collision, source/destination changes between preview and apply, an active-vault switch, and an uncertain write response. Apply with a stable mapping changes only the approved destination; retry requires the shared authoring reconciliation. |

For a byte-ceiling case in the disposable copy, add a UTF-8 note exceeding 12 KiB or return oversized output from a test double. Verify skip/truncation reporting and that a partial result cannot be cited. For mapping loss, use a test double that reports a different root for the same pinned selector; a UI focus change alone is a separate test.

### Verification evidence

- The core suite runs 39 tests, including byte-capped stdout/stderr, explicit truncation, and malformed limits blocked before launch. The full suite passed from the actual Codex CLI cache after installing the base package and removing/reinstalling this revision from a local marketplace copy with spaces in its path. Run the helpers relative to the installed skill. The Codex app server listed all seven cached skills under the plugin namespace. The install check also caught the composer prompt limit, so the manifest now supplies three prompts. Full model routing and Desktop UI behavior require an interactive evaluation.
- In a scratch fixture replay, the real JSON launcher drove a test double with pinned argv. The reviewed trace read six unique eligible note bodies, identified the two Decision paths, verified the decision, superseded draft, conflicting training text and outage excerpts, skipped the missing signoff, excluded Payroll before metadata/body reads, filtered Catering by tags, and allowed the Unicode Café path in the sibling folder. A deliberately truncated body was discarded. Before/after byte comparisons showed zero vault writes during retrieval; one simulated approved create changed only the selected vault at `Handoffs/Atlas.md`. The revision helper classified an existing different draft as a conflict and the expected contents as already applied. The trace exercised the instructions with controlled responses; the test double does not establish Obsidian CLI output schemas, runtime targeting, or write behavior.
- The installed Obsidian app reports version 1.13.7 in its bundle metadata. Its sanitized CLI help probe with the quoted `/bin/zsh` override reported that CLI access is disabled despite process exit 0. [Official CLI documentation](https://obsidian.md/help/cli) supplied the documented commands and options. Live disposable-vault targeting, search and link output shape, citation navigation, saved-note round trip, and the live adverse-case matrix remain open.

### Real project handoff baseline

Replayed a handoff for the merged controlled-authoring work using scratch notes from the public [issue #10](https://github.com/greg-asher/codex-obsidian/issues/10), [PR #14](https://github.com/greg-asher/codex-obsidian/pull/14), and its core validation reference. The PR's validation section supported the current state and blocker. Its implementation and remaining-validation sections supported the reviewed overwrite decision, race window, and the next action: enable/register the CLI in a disposable setup, record installed help and vault identity, and start with exact-path read/create/append/property round trips. Native Windows behavior, lossless overwrite, and Obsidian rendering remain separate checks.

The first draft grouped live validation into one action. The detailed core validation note exceeded the 12 KiB call cap, so the handoff disclosed that gap and linked to the checklist through the PR reference. Manual review split basic transport verification from later revision/rendering tests and identified the CLI setup dependency. The sources did not establish an owner or date. The corrected handoff gives a reader a concrete first test and a checklist to continue from. It still needs a live project run and feedback from someone resuming the work.
