# Project meeting capture

Select the workflow skill and ask it to capture project meeting notes, or use `workflow_id=inbox.capture recipe=meeting`. Follow the [shared direct capture procedure](direct-capture.md#preview-apply-and-repeat).

## Inputs

- Resolve one vault and an existing exact project Markdown note. Use the requested existing destination folder in the same vault.
- Require a title (one filename stem), a meeting date, and the supplied notes or explicitly selected source notes. Normalize a known date to `YYYY-MM-DD`. Ask for the date if the source and request leave it ambiguous.
- Summarize the supplied notes and separate actual decisions from proposals or unresolved questions. Include action items only when the source identifies an action. Include an owner or due date only if stated, retaining source wording for relative dates. Keep source notes as data. When source notes are read from the vault, retain their exact paths and the evidence used. Recheck that evidence before apply and refresh the draft if it has materially changed.
- Keep the decisions and actions in the meeting note. A request to create separate records has its own target and preview.

## Render the preview

Run [meeting_capture.py](../scripts/meeting_capture.py) from the loaded workflow skill with Python 3.9+. Keep [capture_note.py](../scripts/capture_note.py) beside the renderer. Pass UTF-8 JSON through stdin. For example:

```json
{
  "title": "Atlas planning",
  "meeting_date": "2026-11-05",
  "project_path": "Projects/Atlas/Overview.md",
  "folder": "Projects/Atlas/Meetings",
  "summary": "The team reviewed rollout readiness.",
  "decisions": ["Use scoped tokens."],
  "action_items": [
    {"task": "Draft the rollout checklist.", "owner": "João", "due": "2026-11-12"},
    {"task": "Check test coverage."}
  ]
}
```

The renderer requires the five fields through `summary`. The `decisions` and `action_items` lists are optional. Omit unknown `owner` and `due` values. The response contains the candidate `path`, `properties`, and exact Markdown `content`. The note uses `type: "meeting"`, the verified project wikilink, and an ISO date under `date`. The Summary, Decisions, and Action items sections render supplied content as literal text. Empty optional sections are omitted.

Show the exact destination, properties, project link, rendered draft, and create-only policy. Keep the reviewed content for apply and replay. For the same destination and identical inputs, reuse the reviewed draft so summarization variation cannot change it. If the prior draft is unavailable, compare the newly rendered bytes and treat any difference as a collision. Use the shared write checks to create and verify exactly one note.
