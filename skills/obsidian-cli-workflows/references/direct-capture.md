# Direct project capture

Use these checks for the decision and meeting recipes. The workflow owns preview and approval. Navigation verifies the vault, and core authoring executes and verifies the approved write.

## Preview, apply, and repeat

1. Resolve all required inputs. Use the pinned vault to verify the project note exists and the destination folder is contained and already exists. Check the resolved target and any path alias. Stop if the project link would resolve ambiguously, the destination aliases the project note, or the folder/path cannot be verified.
2. Render the draft. Use the [core authoring procedure](../../obsidian-official-cli/references/authoring-and-revision.md) to retain the target, exact expected bytes, and before-state. Check the core launcher's literal-content constraints before offering apply. Preview the project link, properties, exact Markdown, destination, and create-only policy. Preview never writes, even when `output=note`. Inline/JSON controls the report format. A plan-only request may stop before rendering.
3. If the destination already contains the exact rendered bytes, report `already-present` and skip the write. This describes the observed content without attributing it to a prior run. If different or unreadable, report the collision or blocker. A new title or folder is a new preview. An apply request without a matching approved preview produces the preview and waits for approval.
4. With matching approval, revalidate the vault mapping, contained paths, project reference, destination state, and supported `create` options. Delegate a single `create path=...` with the exact approved Markdown as literal content and no overwrite, navigation, or additional property writes. Apply only if the destination remains absent. The same-content check also applies here if another run has created the note in the meantime.
5. Read the exact destination through the pinned CLI and verify complete expected bytes, typed properties, and the intended project reference through the shared authoring contract. Report verified success, already present, conflict, or uncertain completion. After uncertainty, inspect the actual state and use the core retry rules. An absent note alone cannot establish that the original write cannot still happen. Concurrent app writes retain the documented recheck-to-write race.

For another collision policy, route to ordinary authoring and preview that operation separately.
