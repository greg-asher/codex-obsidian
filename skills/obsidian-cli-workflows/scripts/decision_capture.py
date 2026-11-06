"""Render a decision capture candidate from explicit JSON inputs."""

import sys

from capture_note import candidate, main, validate_text


REQUIRED = {"title", "decision", "project_path", "folder"}
OPTIONAL = {"rationale"}


def render(fields):
    if not isinstance(fields, dict) or not REQUIRED <= fields.keys() <= (REQUIRED | OPTIONAL):
        raise ValueError("provide title, decision, project_path and folder, with optional rationale")
    for name, value in fields.items():
        validate_text(name, value)
    sections = [("Decision", fields["decision"])]
    if "rationale" in fields:
        sections.append(("Rationale", fields["rationale"]))
    return candidate(fields, "decision", sections)


if __name__ == "__main__":
    sys.exit(main(render))
