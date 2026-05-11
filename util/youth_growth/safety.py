"""心理健康相关内容的安全筛查（教育场景：非诊断、触发升级建议）。"""
from __future__ import annotations

import re
from typing import Any

# 简体中文高频危机表述（示例集合，需持续运营迭代）
_CRISIS_PATTERNS = [
    r"不想活",
    r"自杀",
    r"自残",
    r"结束生命",
    r"死了算了",
    r"不想活了",
    r"割腕",
    r"跳楼",
]
_COMPILED = [re.compile(p) for p in _CRISIS_PATTERNS]


def scan_text(text: str | None) -> bool:
    if not text or not isinstance(text, str):
        return False
    t = text.strip()
    if len(t) < 2:
        return False
    return any(p.search(t) for p in _COMPILED)


def crisis_from_questionnaire(q: dict[str, Any] | None) -> tuple[bool, list[str]]:
    """返回 (是否触发危机路径, 原因标签)。"""
    if not q:
        return False, []
    reasons: list[str] = []
    notes = q.get("notes") or q.get("free_text") or ""
    if scan_text(str(notes)):
        reasons.append("free_text_keyword")

    try:
        sh = int(q.get("self_harm_signal", 1))
    except (TypeError, ValueError):
        sh = 1
    if sh >= 4:
        reasons.append("self_harm_signal_high")

    return (len(reasons) > 0), reasons


def escalation_message() -> str:
    return (
        "系统检测到可能涉及自伤、自杀或紧急安全风险的内容。"
        "请务必尽快联系家长/监护人、学校心理老师或当地紧急求助热线；"
        "本工具不提供危机干预或医学诊断，请先确保安全。"
    )
