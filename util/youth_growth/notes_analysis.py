"""补充说明（notes）轻量主题分析，用于调整报告叙述与行动建议（关键词规则，非 LLM）。"""
from __future__ import annotations

from typing import Any


def _dimension_level_simple(key: str, value: int) -> str:
    """与 report_builder._dimension_level 一致，避免循环 import。"""
    positive = key == "sleep_quality"
    if positive:
        if value >= 4:
            return "good"
        if value >= 3:
            return "mid"
        return "bad"
    if value >= 4:
        return "bad"
    if value >= 3:
        return "mid"
    return "good"


# (theme_id, 中文主题名, 关键词)
_THEME_DEFS: list[tuple[str, str, tuple[str, ...]]] = [
    (
        "academic",
        "学业与任务节奏",
        ("考试", "成绩", "作业", "补课", "升学", "中考", "高考", "排名", "课业", "测验", "月考", "期末"),
    ),
    (
        "family",
        "家庭互动与期望",
        ("父母", "爸妈", "家里人", "吵架", "离婚", "管教", "唠叨", "期望", "亲子"),
    ),
    (
        "peer",
        "同伴与校园融入",
        ("同学", "朋友", "孤立", "排挤", "霸凌", "融不进", "小团体", "社交"),
    ),
    ("sleep", "作息与睡眠", ("睡眠", "失眠", "睡不着", "熬夜", "作息", "入睡")),
    ("mood", "情绪与心力", ("焦虑", "抑郁", "难过", "想哭", "低落", "烦躁", "心慌", "崩溃")),
]

_THEME_TO_DIMS: dict[str, tuple[str, ...]] = {
    "academic": ("academic_pressure", "attention_focus"),
    "family": ("stress_level", "emotion_dysregulation"),
    "peer": ("social_isolation",),
    "sleep": ("sleep_quality",),
    "mood": ("mood_low_energy", "emotion_dysregulation"),
}

_THEME_ACTIONS: dict[str, str] = {
    "academic": "补充说明侧重学业：先把目标拆到「每日可完成的一小块」，并与孩子共同商定考试季节奏与休息。",
    "family": "补充说明侧重家庭：近期沟通可先处理关系与期待落差，再谈具体行为；固定短时段倾听比长篇说教更有效。",
    "peer": "补充说明侧重同伴：可先确认在校安全感与归属体验，再讨论矛盾细节；必要时请学校中性协调。",
    "sleep": "补充说明侧重作息：把固定入睡与起床作为第一优先级，睡前减少评判性对话与屏幕刺激。",
    "mood": "补充说明侧重情绪：以命名感受与降速回应为主，必要时寻求专业评估；避免用「想开点」一笔带过。",
}


def analyze_supplementary_notes(
    notes_text: str,
    *,
    dimensions: dict[str, int] | None = None,
) -> dict[str, Any]:
    """
    从补充说明中抽取主题，生成可并入报告的短句与行动注入（不改变问卷计分）。
    dimensions: 若传入，仅对「需关注/重点关注」的维度做沟通排序加权。
    """
    raw = str(notes_text or "").strip()
    if not raw:
        return {
            "has_notes": False,
            "snippet": "",
            "detected_themes": [],
            "theme_ids": [],
            "adjustment_summary": "",
            "action_injections": [],
            "emphasis_dimension_keys": [],
            "extra_recommended_actions": [],
        }

    snippet = raw if len(raw) <= 160 else raw[:157] + "…"
    scored: list[tuple[str, str, int]] = []
    for tid, label, kws in _THEME_DEFS:
        score = sum(1 for kw in kws if kw in raw)
        if score > 0:
            scored.append((tid, label, score))
    scored.sort(key=lambda x: -x[2])

    theme_ids = [t[0] for t in scored]
    detected = [t[1] for t in scored]

    if not detected:
        return {
            "has_notes": True,
            "snippet": snippet,
            "detected_themes": [],
            "theme_ids": [],
            "adjustment_summary": f"补充说明已收录，未匹配到预设主题标签；家校沟通可直接围绕原文：{snippet}",
            "action_injections": [],
            "emphasis_dimension_keys": [],
            "extra_recommended_actions": [
                f"结合补充说明原文，近期沟通可优先澄清孩子最困扰的具体情境：{snippet}"
            ],
        }

    theme_part = "、".join(detected[:3])
    adjustment_summary = (
        f"结合补充说明，叙述与建议已侧重以下情境（关键词规则，非诊断）：{theme_part}。"
    )

    action_injections: list[str] = []
    extra_recommended: list[str] = []
    seen: set[str] = set()
    for tid, _label, _s in scored[:2]:
        line = _THEME_ACTIONS.get(tid)
        if line and line not in seen:
            seen.add(line)
            action_injections.append(line)
            extra_recommended.append(line)

    emphasis_keys: list[str] = []
    if dimensions:
        dims = {k: int(v) for k, v in dimensions.items() if isinstance(v, int)}
        for tid, _label, _s in scored:
            for dk in _THEME_TO_DIMS.get(tid, ()):
                if dk not in dims or dk in emphasis_keys:
                    continue
                if _dimension_level_simple(dk, dims[dk]) in ("bad", "mid"):
                    emphasis_keys.append(dk)

    return {
        "has_notes": True,
        "snippet": snippet,
        "detected_themes": detected,
        "theme_ids": theme_ids,
        "adjustment_summary": adjustment_summary,
        "action_injections": action_injections,
        "emphasis_dimension_keys": emphasis_keys,
        "extra_recommended_actions": extra_recommended,
    }
