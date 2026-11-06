"""Run the deterministic plugin and packaging checks without Obsidian."""
import csv
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_manifests():
    manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    plugin, = marketplace["plugins"]
    require(plugin["name"] == manifest["name"] == "codex-obsidian", "plugin names disagree")
    require(plugin["source"]["source"] == "local", "expected local marketplace source")
    require((ROOT / plugin["source"]["path"]).resolve() == ROOT, "marketplace must point to plugin root")
    require((ROOT / manifest["skills"]).resolve() == SKILLS, "unexpected skill root")
    interface = manifest["interface"]
    require(0 < len(interface["defaultPrompt"]) <= 3, "expected one to three default prompts")
    for key in ("composerIcon", "logo"):
        require((ROOT / interface[key]).is_file(), f"missing {key} asset")


def check_skills():
    for directory in sorted(path for path in SKILLS.iterdir() if path.is_dir()):
        text = (directory / "SKILL.md").read_text(encoding="utf-8")
        metadata = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.DOTALL)
        require(metadata, f"missing frontmatter in {directory.name}")
        skill = yaml.safe_load(metadata[1])
        require(skill["name"] == directory.name and skill["description"].strip(),
                f"invalid skill metadata in {directory.name}")
        agent = yaml.safe_load((directory / "agents/openai.yaml").read_text(encoding="utf-8"))
        require(agent["policy"]["allow_implicit_invocation"] is False,
                f"expected explicit invocation for {directory.name}")
        for key in ("display_name", "short_description", "default_prompt"):
            require(agent["interface"][key].strip(), f"missing {key} in {directory.name}")


def check_evaluations():
    evaluations = sorted(SKILLS.glob("*/assets/*eval*.csv"))
    require(evaluations, "no evaluation CSVs found")
    for path in evaluations:
        with path.open(encoding="utf-8", newline="") as stream:
            header, *rows = csv.reader(stream, strict=True)
        require(header[0] == "id" and rows, f"missing evaluation IDs in {path}")
        require(all(len(row) == len(header) for row in rows), f"malformed CSV row in {path}")
        ids = [row[0] for row in rows]
        require(all(ids) and len(set(ids)) == len(ids), f"missing or duplicate IDs in {path}")


def check_links():
    documents = [ROOT / "README.md", *ROOT.glob("docs/**/*.md"), *SKILLS.rglob("*.md")]
    for path in documents:
        for link in re.findall(r"\]\(([^)\n]+)\)", path.read_text(encoding="utf-8")):
            if not re.match(r"[.a-zA-Z]", link):
                continue
            target = urlsplit(link)
            if not target.scheme and target.path:
                require((path.parent / unquote(target.path)).exists(),
                        f"broken local link in {path.relative_to(ROOT)}: {link}")


def check_workflows():
    registry = SKILLS / "obsidian-cli-workflows/references/workflow-registry.md"
    text = registry.read_text(encoding="utf-8")
    entries = re.findall(r"^### (\d+)\) `([\w.]+)`$", text, re.MULTILINE)
    ids = [name for _, name in entries]
    internal = re.findall(r"^- `internal_id`: `(\w+)`$", text, re.MULTILINE)
    require(ids and len(ids) == len(set(ids)) == len(internal) == len(set(internal)),
            "missing or duplicate workflow IDs")
    require([int(number) for number, _ in entries] == list(range(1, len(ids) + 1)),
            "workflow numbering is out of order")
    return len(ids)


def main():
    check_manifests()
    check_skills()
    check_evaluations()
    check_links()
    count = check_workflows()
    print(f"Package checks passed for {count} workflows.", flush=True)
    suites = sorted(SKILLS.glob("*/tests"))
    require(suites, "no skill test suites found")
    for directory in suites:
        print(f"Running {directory.parent.name} tests", flush=True)
        subprocess.run([sys.executable, "-B", "-m", "unittest", "discover", "-s", str(directory)],
                       cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
