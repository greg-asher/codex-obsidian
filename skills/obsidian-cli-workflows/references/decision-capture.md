# Project decision capture

Use the bundled `decision` recipe through `workflow_id=inbox.capture recipe=decision` or an explicit request to capture a project decision after selecting the workflow skill. This recipe creates one note with create-only behavior. The workflow skill owns input resolution and the preview. Navigation owns vault discovery. Core authoring owns the CLI call, verification, and recovery.

## Inputs and rendered note

| Input | Requirement |
| --- | --- |
| `vault` | Resolve and pin the vault selector and canonical root through navigation. A missing selector can resolve to one unambiguous vault. |
| `project_path` | An existing, exact vault-relative Markdown project note. A project name may be resolved by scoped read-only discovery. Ask for a selection when ambiguous. |
| `folder` | The requested existing destination folder inside that vault. Ask when unknown. |
| `title` | One filename stem, without an extension. Preserve the user's wording. Ask for a safe alternative when invalid. |
| `decision` | The decision to record. Use supplied or explicitly selected text. |
| `rationale` | Optional supplied rationale. Omit the section when absent. |

The destination is `<folder>/<title>.md`. Use a stable title for repeats. No timestamps or random suffixes are added. The fixed template has two frontmatter text values, `type: "decision"` and `project: "[[<project_path>]]"`, plus a Decision section and optional Rationale. Preserve the decision and rationale as literal text blocks so pasted links, embeds, and markup cannot become active content. Only the resolved project link is generated as a wikilink. If existing vault property types conflict with the recipe, explain the conflict before any write.

Use [decision_capture.py](../scripts/decision_capture.py), Python 3.9+ standard library, to render the candidate. Resolve the script from the loaded workflow skill. Pass a UTF-8 JSON object via stdin with `title`, `decision`, `project_path`, `folder`, and optional `rationale`. Use a JSON serializer and literal arguments. The helper returns `path`, `properties`, and exact Markdown `content`. It only validates lexical input and renders. The agent still verifies canonical containment, actual filenames and normalization aliases, project identity, property types, and permissions.

Follow the shared [direct capture procedure](direct-capture.md#preview-apply-and-repeat). This recipe handles one direct decision capture.
