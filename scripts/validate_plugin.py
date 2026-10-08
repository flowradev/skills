#!/usr/bin/env python3
"""Validate Cursor plugin packaging and Flowra skill frontmatter."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def load_json(rel: str) -> dict:
    path = ROOT / rel
    if not path.is_file():
        fail(f"missing {rel}")
        return {}
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        fail(f"{rel}: invalid JSON ({exc})")
        return {}
    if not isinstance(data, dict):
        fail(f"{rel}: expected a JSON object")
        return {}
    return data


def check_paths(manifest: dict) -> None:
    for key in ("logo", "skills", "rules", "commands", "mcpServers"):
        rel = manifest.get(key)
        if not isinstance(rel, str):
            fail(f"plugin.json.{key} must be a relative path string")
            continue
        if rel.startswith("/") or ".." in Path(rel).parts:
            fail(f"plugin.json.{key} must be a relative path without ..")
            continue
        target = ROOT / rel
        if not target.exists():
            fail(f"plugin.json.{key} points at missing path {rel}")


def check_skill(rel: str, expected_name: str) -> str:
    skill = ROOT / rel
    if not skill.is_file():
        fail(f"missing {rel}")
        return ""
    text = skill.read_text()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        fail(f"{rel} is missing YAML frontmatter")
        return text
    fm = match.group(1)
    if not re.search(rf"^name:\s*{re.escape(expected_name)}\s*$", fm, re.M):
        fail(f"{rel} frontmatter name must be {expected_name}")
    desc = None
    folded = re.search(r"^description:\s*>\n((?:  .*\n)+)", fm, re.M)
    if folded:
        desc = " ".join(line.strip() for line in folded.group(1).splitlines() if line.strip())
    else:
        inline = re.search(r"^description:\s*(.+)$", fm, re.M)
        desc = inline.group(1).strip() if inline else None
    if not desc:
        fail(f"{rel} description is empty")
    elif len(desc) > 1024:
        fail(f"{rel} description is {len(desc)} chars (max 1024)")
    if "metadata:" in fm and not re.search(r'version:\s*"?0\.\d+', fm):
        fail(f"{rel} metadata.version is missing")
    lines = text.splitlines()
    if len(lines) > 500:
        fail(f"{rel} is {len(lines)} lines (keep under 500)")
    return text


def check_evals() -> None:
    evals = ROOT / "evals"
    if not evals.is_dir():
        fail("missing evals/")
        return
    files = sorted(evals.glob("*.json"))
    if len(files) < 6:
        fail(f"evals/ has {len(files)} scenarios (need at least 6)")
    required_ids = {
        "operate-email-confirm",
        "build-cron-workflow",
        "build-agent-widget",
        "debug-paused",
        "connection-initiated",
        "custom-toolkit",
    }
    seen: set[str] = set()
    for path in files:
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            fail(f"{path.relative_to(ROOT)}: invalid JSON ({exc})")
            continue
        for key in ("id", "skill", "query", "expected_behavior"):
            if key not in data:
                fail(f"{path.name} missing {key}")
        if not isinstance(data.get("expected_behavior"), list) or not data.get("expected_behavior"):
            fail(f"{path.name} expected_behavior must be a non-empty list")
        seen.add(str(data.get("id") or ""))
    missing = required_ids - seen
    if missing:
        fail("evals missing ids: " + ", ".join(sorted(missing)))


def check_examples(skill_text: str) -> None:
    examples = ROOT / "skills/flowra/references/examples.md"
    if not examples.is_file():
        fail("missing skills/flowra/references/examples.md")
        return
    text = examples.read_text()
    required = (
        '"mode": "connect"',
        '"reinitiateAll": false',
        '"syncResponseToWorkbench": false',
        '"allowExecuteWhenInactive": false',
        '"outputSchema"',
        "rank.text",
        "<sendSlug from DISCOVER>",
        "<slackSlug from DISCOVER>",
    )
    for needle in required:
        if needle not in text:
            fail(f"examples.md is missing required snippet: {needle}")
    if "do not FLOWRA_EXECUTE_WORKFLOW on an agent" in skill_text.lower():
        fail("SKILL.md still claims EXECUTE_WORKFLOW fails on agents")
    banned = (
        "builder pins",
        "sdks/cli",
        "pip install flowra\n",
    )
    refs = (ROOT / "skills/flowra").rglob("*.md")
    blob = "\n".join(p.read_text() for p in refs)
    if "Prefer MCP with builder pins" in blob:
        fail("skill still treats builder pins as the default path")
    if "sdks/cli" in blob:
        fail("cli.md still points at sdks/cli")
    if "10_000" in blob and "credits" in blob:
        fail("billing still invents a credit-to-dollar ratio")


def main() -> int:
    manifest = load_json(".cursor-plugin/plugin.json")
    if manifest:
        if manifest.get("name") != "flowra":
            fail("plugin.json.name must be flowra")
        if manifest.get("version") != "0.2.0":
            fail("plugin.json.version must be 0.2.0")
        check_paths(manifest)
    for mcp_rel in ("mcp.json", ".mcp.json"):
        mcp = load_json(mcp_rel)
        servers = mcp.get("mcpServers") if mcp else None
        if not isinstance(servers, dict) or "flowra" not in servers:
            fail(f"{mcp_rel} must define mcpServers.flowra")
        elif servers.get("flowra", {}).get("url") != "https://mcp.flowra.dev/mcp":
            fail(f"{mcp_rel} flowra.url must be https://mcp.flowra.dev/mcp")
        elif "headers" in servers.get("flowra", {}):
            fail(f"{mcp_rel} must not ship API-key headers")

    server = load_json("server.json")
    if server:
        if server.get("name") != "io.github.flowradev/mcp":
            fail("server.json.name must be io.github.flowradev/mcp")
        remotes = server.get("remotes") or []
        if not remotes or remotes[0].get("url") != "https://mcp.flowra.dev/mcp":
            fail("server.json remotes[0].url must be https://mcp.flowra.dev/mcp")
        if len(server.get("description") or "") > 100:
            fail("server.json description exceeds 100 characters")

    for rel in (
        "LICENSE",
        "README.md",
        "CHANGELOG.md",
        "llms.txt",
        "assets/logo.svg",
        "assets/logo-400.png",
        "assets/social-preview.png",
        "rules/flowra-safety.mdc",
        "skills/flowra/references/workbench.md",
        "skills/flowra-onboard/SKILL.md",
        "commands/flowra-setup.md",
        "commands/flowra-status.md",
        ".claude-plugin/plugin.json",
        ".codex-plugin/plugin.json",
    ):
        if not (ROOT / rel).is_file():
            fail(f"missing {rel}")

    skill_text = check_skill("skills/flowra/SKILL.md", "flowra")
    check_skill("skills/flowra-onboard/SKILL.md", "flowra-onboard")
    if skill_text:
        check_examples(skill_text)
    check_evals()

    if errors:
        print("validate_plugin: FAIL")
        for item in errors:
            print(f"  - {item}")
        return 1
    print("validate_plugin: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
