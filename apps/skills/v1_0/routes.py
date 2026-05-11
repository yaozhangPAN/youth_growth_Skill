"""Skills v1_0：列表与 invoke。"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from flask import jsonify, request

from apps.skills.v1_0 import blueprint
from util.skill_registry import get_registry


def _parse_invoke_body() -> tuple[str, dict[str, Any]]:
    data = request.get_json(silent=True) or {}
    user_input = ""
    if isinstance(data.get("input"), str):
        user_input = data["input"]
    kwargs = {k: v for k, v in data.items() if k != "input"}
    return user_input, kwargs


def _frontmatter_description(skill_dir: Path) -> str | None:
    md = skill_dir / "SKILL.md"
    if not md.exists():
        return None
    text = md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    for line in parts[1].splitlines():
        if line.startswith("description:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return None


@blueprint.post("/skills/v1_0/list")
def list_skills():
    reg = get_registry()
    root = Path(__file__).resolve().parents[3] / "skills" / "internal"
    items = []
    for name in sorted(reg.keys()):
        skill_dir = root / name
        desc = _frontmatter_description(skill_dir) if skill_dir.is_dir() else None
        items.append(
            {
                "name": name,
                "description": desc or getattr(reg[name], "description", ""),
                "version": getattr(reg[name], "version", "1.0.0"),
            }
        )
    return jsonify({"code": 200, "msg": "success!", "data": {"skills": items}}), 200


@blueprint.post("/skills/v1_0/<name>/invoke")
def invoke(name: str):
    reg = get_registry()
    skill = reg.get(name)
    if skill is None:
        return jsonify({"code": 404, "msg": f"skill not found: {name}", "data": {}}), 404
    user_input, kwargs = _parse_invoke_body()
    try:
        out = skill.run(user_input, **kwargs)
    except Exception as exc:  # pragma: no cover
        return jsonify({"code": 500, "msg": str(exc), "data": {}}), 500

    parsed: Any
    try:
        parsed = json.loads(out)
    except json.JSONDecodeError:
        parsed = {"raw": out}

    return jsonify({"code": 200, "msg": "success!", "data": {"output": parsed}}), 200
