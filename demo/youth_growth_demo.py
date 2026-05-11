#!/usr/bin/env python3
"""独立演示：不启动 HTTP，直接调用 Skill 内核。"""
from __future__ import annotations

import argparse
import json
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)


def main() -> None:
    parser = argparse.ArgumentParser(description="Youth growth assessment demo")
    parser.add_argument(
        "-i",
        "--input",
        default=os.path.join(_ROOT, "demo", "sample_input.json"),
        help="Path to JSON payload (birth + questionnaire)",
    )
    args = parser.parse_args()

    from util.skill_registry import reload_registry

    reload_registry()
    from util.skill_registry import get_registry

    reg = get_registry()
    skill = reg.get("youth_growth_assessment")
    if skill is None:
        print("Skill youth_growth_assessment not found.", file=sys.stderr)
        sys.exit(1)

    with open(args.input, encoding="utf-8") as f:
        payload = json.load(f)

    out = skill.run(json.dumps(payload, ensure_ascii=False))
    print(out)


if __name__ == "__main__":
    main()
