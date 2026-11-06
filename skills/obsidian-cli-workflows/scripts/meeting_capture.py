"""Render a meeting capture candidate from reviewed meeting fields."""

from datetime import date
import sys

from capture_note import candidate, main, validate_text


REQUIRED = {"title", "meeting_date", "summary", "project_path", "folder"}
OPTIONAL = {"decisions", "action_items"}


def list_field(fields, name):
    value = fields.get(name, [])
    if not isinstance(value, list):
        raise ValueError(f"{name} must be a list")
    return value


def action_text(item):
    if not isinstance(item, dict) or "task" not in item or item.keys() - {"task", "owner", "due"}:
        raise ValueError("each action item needs task, with optional owner and due")
    for name, value in item.items():
        validate_text(name, value)
    parts = [item["task"]]
    if "owner" in item:
        parts.append(f"Owner: {item['owner']}")
    if "due" in item:
        parts.append(f"Due: {item['due']}")
    return " | ".join(parts)


def render(fields):
    if not isinstance(fields, dict) or not REQUIRED <= fields.keys() <= (REQUIRED | OPTIONAL):
        raise ValueError("provide title, meeting_date, summary, project_path and folder")
    for name in REQUIRED:
        validate_text(name, fields[name])
    meeting_date = fields["meeting_date"]
    try:
        if date.fromisoformat(meeting_date).isoformat() != meeting_date:
            raise ValueError
    except ValueError:
        raise ValueError("meeting_date must be a valid YYYY-MM-DD calendar date") from None

    sections = [("Summary", fields["summary"])]
    decisions = list_field(fields, "decisions")
    for decision in decisions:
        validate_text("decision", decision)
    if decisions:
        sections.append(("Decisions", "\n".join(f"- {decision}" for decision in decisions)))
    actions = list_field(fields, "action_items")
    if actions:
        sections.append(("Action items", "\n".join(f"- {action_text(item)}" for item in actions)))
    return candidate(fields, "meeting", sections, date=meeting_date)


if __name__ == "__main__":
    sys.exit(main(render))
