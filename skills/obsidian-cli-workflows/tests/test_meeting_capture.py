import json
from pathlib import Path
import subprocess
import sys
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "meeting_capture.py"


class MeetingCaptureTests(unittest.TestCase):
    def setUp(self):
        self.fields = {
            "title": "Atlas planning – João",
            "meeting_date": "2026-11-05",
            "summary": "Reviewed rollout readiness.\n![[Private.md]]",
            "project_path": "Projects/Atlas/Overview.md",
            "folder": "Projects/Atlas/Meetings",
        }

    def invoke(self):
        return subprocess.run(
            [sys.executable, str(SCRIPT)],
            input=json.dumps(self.fields).encode("utf-8"),
            capture_output=True,
        )

    def test_render_retains_stated_values_and_keeps_source_markup_literal(self):
        self.fields.update(
            decisions=["Use scoped tokens."],
            action_items=[
                {"task": "Draft checklist.", "owner": "João", "due": "2026-11-12"},
                {"task": "Check coverage."},
            ],
        )
        first = self.invoke()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, self.invoke().stdout)
        note = json.loads(first.stdout)
        self.assertEqual(note["path"], "Projects/Atlas/Meetings/Atlas planning – João.md")
        self.assertEqual(note["properties"], {
            "type": "meeting", "project": "[[Projects/Atlas/Overview.md]]", "date": "2026-11-05",
        })
        self.assertIn(
            "    ![[Private.md]]\n\n## Decisions\n\n    - Use scoped tokens.\n"
            "\n## Action items\n\n    - Draft checklist. | Owner: João | Due: 2026-11-12\n"
            "    - Check coverage.\n",
            note["content"],
        )

    def test_summary_only_does_not_generate_decisions_or_actions(self):
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        note = json.loads(result.stdout)["content"]
        self.assertNotIn("## Decisions", note)
        self.assertNotIn("## Action items", note)

    def test_invalid_date_action_and_escaping_destination_are_rejected(self):
        for changes in (
            {"meeting_date": "2026-02-30"},
            {"meeting_date": "20261105"},
            {"action_items": [{"owner": "João"}]},
            {"decisions": "Use scoped tokens."},
            {"folder": "Projects/../Private"},
        ):
            with self.subTest(changes=changes):
                old = self.fields.copy()
                self.fields.update(changes)
                result = self.invoke()
                self.assertEqual(result.returncode, 1)
                self.assertEqual(result.stdout, b"")
                self.fields = old
