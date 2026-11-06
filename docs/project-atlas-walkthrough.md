# Project Atlas walkthrough

Project Atlas is a fictional authentication rollout. You’ll review its decision and production blocker, approve one note update, and see the result in Bases.

## Set up the plugin and vault

1. Clone the repository with `git clone https://github.com/greg-asher/codex-obsidian.git`. Open the checkout as a local project in Codex, then install **Codex Obsidian** from **LumiCorp's Marketplace** in the plugin directory. Restart Codex if the repo marketplace does not appear. If you use the Codex CLI, the equivalent setup from the checkout is:

   ```sh
   codex plugin marketplace add .
   codex plugin add codex-obsidian@lumicorp-marketplace
   ```

   Select **Obsidian CLI Workflows** explicitly when starting the review. Codex loads the installed copy from its plugin cache. After updating the checkout, refresh or reinstall the plugin and start a new session. [OpenAI local plugin documentation](https://developers.openai.com/plugins/build/plugins#install-a-local-plugin-manually)

2. Copy [Project Atlas](../examples/Project%20Atlas/) to a separate, writable location. Keep the folder name `Project Atlas` for the prompts below. In Obsidian, choose **Open folder as vault** and select the copied folder, which contains the `Atlas` subfolder. If another vault already uses that name, name the copy differently and substitute that name in the prompts and commands. The sample includes the notes and dashboard. Enable the **Bases** core plugin if it is disabled.

3. In Obsidian, enable and register **Command line interface** under **Settings → General**. Keep Obsidian running. Open a new terminal and run:

   ```sh
   obsidian version
   obsidian vault="Project Atlas" vault info=path
   ```

   Check that the second command returns the path of your copy. On Windows, use the official `Obsidian.com` terminal redirector. If the CLI is missing or reports that it is disabled, follow the official setup steps. Use Python 3.9 or later for the bundled helpers. If Codex on macOS reports that its Zsh path is unavailable, follow the [Zsh override instructions](../README.md#macos-zsh-path-override). [Obsidian CLI setup](https://obsidian.md/help/cli)

## Review and preview

In a Codex chat with **Obsidian CLI Workflows** selected, ask:

> In the Project Atlas vault, review the Atlas folder. Summarize the current sign-in decision, what is blocking production, and which follow-up is ready to close. Cite each finding with the exact note path and heading. Preview the exact edit to the ready action, explain how it would be written, and keep the vault read-only. Show any remaining open work.

Check the review against the sample:

| Expected finding | Source |
| --- | --- |
| OIDC was approved for employee sign-in. API clients still use service tokens. | `Atlas/Decision.md` › Decision |
| OIDC worked in staging. Production still needs a security review of the redirect URI list. | `Atlas/Rollout.md` › Implementation |
| Ana confirmed ownership. Recording that handoff can close. The review itself stays open. | `Atlas/Rollout.md` › Next actions |

Check the proposed diff. The only intended change is `status: open` → `status: done` in `Atlas/Work/Record redirect review owner.md`. The preview should identify the exact vault and note, disclose the whole-file CLI write used to transport the reviewed edit, and leave both actions open. If the review gives a recommendation without an exact diff, select **Obsidian Official CLI** and ask it to preview that specific status edit, preserving all other text.

## Approve one edit and check Bases

Open `Atlas/Project review.base` in Obsidian. **Open work** starts with two rows. In the same Codex conversation, select **Obsidian Official CLI** for the note revision and approve only the reviewed edit to `Atlas/Work/Record redirect review owner.md`. Check the exact path, written status, and verification in the result. If the note changed since preview, review the refreshed diff before proceeding.

Return to the Base. **Open work** should now show only **Review redirect URI list**. **All work** should still show both actions, with the ownership action marked `done` and the security review still `open`. To verify through the CLI, use the exact view names:

```sh
obsidian vault="Project Atlas" base:query path="Atlas/Project review.base" view="Open work" format=json
obsidian vault="Project Atlas" base:query path="Atlas/Project review.base" view="All work" format=json
```

Run the query again to confirm the same result. If the write response was lost, read the action and verify its status before retrying.

## Follow the citations in Obsidian

Select **Obsidian CLI Workflows** and ask Codex to preview saving the review to a new `Atlas Review.md` at the root of the same vault. Ask for Obsidian wikilinks to the cited paths and headings. Approve that separate create after reviewing its contents. Open the saved note in Obsidian Reading view and follow the decision and rollout citations. They should take you to `Atlas/Decision.md` and `Atlas/Rollout.md`. The rollout note should still describe the production blocker.

To start over, close the sample vault and open another fresh copy from the repository. Use that copy’s exact vault name if you rename the folder.

## Maintainer verification

Use an isolated Codex install and a new copy of the sample vault. Record the OS and Obsidian desktop and installer versions. Confirm the scoped review against the expected findings, compare the vault before and after preview, verify the approved write against the exact diff, follow the saved citations in Obsidian, and check both Bases views before and after apply.

Run the deterministic suites and package checks locally with the same commands used by [GitHub Actions](../.github/workflows/checks.yml):

```sh
python -m pip install "PyYAML==6.0.3"
python -B .github/check.py
```

The automated checks run without a desktop app. Record live walkthrough results separately.

The reference run used macOS 26.6.2, Codex CLI 0.162.1, and Obsidian desktop and installer 1.15.0. A fresh local marketplace install supplied the cached skills and launcher. The installed workflow produced the expected cited review and one-line diff using live, read-only calls to the disposable vault. The cached authoring helpers then applied and verified the exact status change. Both Bases views returned the expected rows on repeated queries. The saved review rendered its wikilinks, and Obsidian resolved their paths and heading targets. Manual click-through from the saved review confirmed that the decision citation opened `Atlas/Decision.md` at **Decision** and the blocker citation opened `Atlas/Rollout.md` at **Implementation**.
