"""Detailed report builder for education-facing narratives."""
from __future__ import annotations

from typing import Any


_DIMENSION_META: dict[str, dict[str, Any]] = {
    "emotion_dysregulation": {
        "label": "情绪调节困难",
        "positive": False,
        "high": "情绪波动偏明显，建议减少对抗式沟通并建立情绪降温流程。",
        "mid": "情绪调节有波动，适合用固定作息和情绪命名练习稳定节奏。",
        "low": "情绪总体较稳，可继续保持表达与复盘习惯。",
    },
    "stress_level": {
        "label": "压力水平",
        "positive": False,
        "high": "压力负担较高，需优先做任务拆解和减压安排。",
        "mid": "存在中等压力，建议每周固定安排恢复性活动。",
        "low": "压力可控，建议维持稳定学习节律。",
    },
    "social_isolation": {
        "label": "社交疏离",
        "positive": False,
        "high": "社交支持偏弱，建议主动连接同伴与可信任成人。",
        "mid": "社交状态一般，可通过小组合作提升归属感。",
        "low": "社交连接较稳定，可继续强化正向互动。",
    },
    "academic_pressure": {
        "label": "学业压力",
        "positive": False,
        "high": "学业压力较大，建议降低一次性目标，转为阶段目标。",
        "mid": "学业压力中等，适合用周计划降低焦虑。",
        "low": "学业压力可控，可保持稳步推进。",
    },
    "sleep_quality": {
        "label": "睡眠质量",
        "positive": True,
        "high": "睡眠质量较好，是当前心理恢复的重要保护因素。",
        "mid": "睡眠一般，建议固定入睡时间并减少夜间刺激。",
        "low": "睡眠不足已影响稳定性，建议把睡眠作为第一优先级。",
    },
    "attention_focus": {
        "label": "专注困难",
        "positive": False,
        "high": "专注困难较明显，建议使用番茄时段和环境减干扰策略。",
        "mid": "专注状态有波动，可通过短周期任务稳定注意力。",
        "low": "专注状态较好，可增加深度学习时段。",
    },
    "mood_low_energy": {
        "label": "低落无力",
        "positive": False,
        "high": "低落和疲惫感偏明显，建议优先恢复作息与运动。",
        "mid": "动力阶段性下降，建议从小任务启动恢复掌控感。",
        "low": "情绪能量总体良好，可保持节奏。",
    },
    "risk_behaviors": {
        "label": "风险行为倾向",
        "positive": False,
        "high": "冲动或冒险倾向偏高，需强化规则边界与复盘机制。",
        "mid": "偶发冲动行为，建议提前约定应对预案。",
        "low": "风险行为总体可控，继续保持明确边界。",
    },
    "self_harm_signal": {
        "label": "自伤信号",
        "positive": False,
        "high": "已出现较高风险信号，建议尽快转专业支持渠道。",
        "mid": "存在一定风险线索，建议持续观察并寻求专业评估。",
        "low": "未见明显自伤风险信号，仍需持续关注。",
    },
}


def _risk_label(tier: str) -> str:
    return {"low": "低风险", "medium": "中风险", "high": "高风险"}.get(tier, tier)


def _dimension_level(key: str, value: int) -> str:
    positive = bool(_DIMENSION_META.get(key, {}).get("positive", False))
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


def _dimension_message(key: str, level: str) -> str:
    meta = _DIMENSION_META.get(key, {})
    if level == "bad":
        return str(meta.get("high", "该维度需要重点关注。"))
    if level == "mid":
        return str(meta.get("mid", "该维度处于中等水平，可持续观察。"))
    return str(meta.get("low", "该维度整体稳定。"))


def _dimension_level_label(level: str) -> str:
    return {"good": "稳定/保护", "mid": "需关注", "bad": "重点关注"}.get(level, "需关注")


def _top_concerns(dimensions: dict[str, int]) -> list[str]:
    concern_pairs: list[tuple[str, float]] = []
    for key, value in dimensions.items():
        if key == "sleep_quality":
            severity = float(6 - int(value))
        else:
            severity = float(value)
        concern_pairs.append((key, severity))
    concern_pairs.sort(key=lambda x: x[1], reverse=True)
    out: list[str] = []
    for key, _score in concern_pairs[:3]:
        label = _DIMENSION_META.get(key, {}).get("label", key)
        out.append(str(label))
    return out


def _timeline_comment(year_item: dict[str, Any]) -> str:
    focus = int(year_item.get("learning_focus", 3))
    wellbeing = int(year_item.get("wellbeing_hint", 3))
    if focus <= 2 or wellbeing <= 2:
        return "建议减负稳节奏，先保作息和情绪稳定。"
    if focus >= 5 and wellbeing >= 4:
        return "适合强化优势科目或项目挑战，但仍需防止过载。"
    return "维持稳定推进，关注阶段性复盘与小步优化。"


def build_detailed_report(
    *,
    scores: dict[str, Any],
    profile: dict[str, Any],
    curve: list[dict[str, Any]],
    peaks_troughs: dict[str, list[int]],
    crisis: bool,
    crisis_reasons: list[str],
    element_resolution: str,
) -> dict[str, Any]:
    dims = scores.get("dimensions", {}) if isinstance(scores, dict) else {}
    tier = str(scores.get("risk_tier", "medium"))
    wellbeing = scores.get("mental_wellbeing_score")
    flags = scores.get("flags", [])

    dimension_analysis: list[dict[str, Any]] = []
    for key, value in dims.items():
        if not isinstance(value, int):
            continue
        level = _dimension_level(key, value)
        dimension_analysis.append(
            {
                "key": key,
                "label": _DIMENSION_META.get(key, {}).get("label", key),
                "value": value,
                "level": _dimension_level_label(level),
                "interpretation": _dimension_message(key, level),
            }
        )

    top_focus = _top_concerns({k: v for k, v in dims.items() if isinstance(v, int)})
    peak_years = peaks_troughs.get("peak_years", [])
    trough_years = peaks_troughs.get("trough_years", [])
    forecast_scores = [
        float((row.get("forecast_indices") or {}).get("overall_index", 3))
        for row in curve
    ]
    forecast_peak_years: list[int] = []
    forecast_trough_years: list[int] = []
    if forecast_scores:
        max_score = max(forecast_scores)
        min_score = min(forecast_scores)
        for idx, row in enumerate(curve):
            year = int(row.get("year", 0))
            score = forecast_scores[idx]
            if score == max_score:
                forecast_peak_years.append(year)
            if score == min_score:
                forecast_trough_years.append(year)
    resolution_text = {
        "explicit_override": "使用了显式指定的五行类型",
        "birth_bazi_with_hour": "根据出生小时换算时辰，按完整八字四柱计算五行倾向",
        "birth_day_stem": "根据出生日期计算日干后映射五行",
        "questionnaire_affinities": "根据兴趣倾向问卷推断",
        "questionnaire_default": "使用默认问卷推断",
    }.get(element_resolution, element_resolution)

    key_findings = [
        f"当前综合风险等级为{_risk_label(tier)}，心理健康观察分为 {wellbeing}。",
        f"需要优先关注的维度：{ '、'.join(top_focus) if top_focus else '暂无' }。",
        f"成长曲线高峰年份：{peak_years or '暂无'}；低谷年份：{trough_years or '暂无'}。",
        f"流年预测曲线高峰年份：{forecast_peak_years or '暂无'}；低谷年份：{forecast_trough_years or '暂无'}。",
    ]
    if crisis:
        key_findings.insert(0, "检测到潜在危机信号，需优先执行安全支持与专业转介。")

    timeline = []
    for row in curve:
        year = row.get("year")
        timeline.append(
            {
                "year": year,
                "psych_state": row.get("psych_state", ""),
                "learning_focus": row.get("learning_focus"),
                "wellbeing_hint": row.get("wellbeing_hint"),
                "forecast_indices": row.get("forecast_indices", {}),
                "focus_comment": _timeline_comment(row),
                "family_action": row.get("guidance", ""),
                "watchout": row.get("concern", ""),
            }
        )

    action_plan = {
        "next_2_weeks": [
            "固定睡眠窗口（建议保证稳定入睡时间），优先恢复基础节律。",
            "把学习目标拆成 15-30 分钟小任务，减少拖延与对抗。",
            "每周至少 1 次无评判沟通，先听感受再谈改进。",
        ],
        "month_1_to_3": [
            "建立家校协同反馈节奏（建议每 2-4 周复盘一次）。",
            "围绕优势科目建立正反馈，避免只盯短板。",
            "在高压力周期保留运动与同伴互动，防止长期内耗。",
        ],
        "escalation": [
            "若出现明显自伤/自杀相关表达或行为，请立即转专业支持渠道。",
            "若连续 2-4 周状态持续恶化，建议尽快进行专业评估。",
        ],
    }
    if crisis:
        action_plan["next_2_weeks"] = [
            "立即确保人身安全，避免单独处于高风险环境。",
            "第一时间联系监护人、学校心理老师或当地专业机构。",
            "暂停以成绩为中心的沟通，优先稳定安全与情绪。",
        ]

    return {
        "overview": "本报告用于教育场景下的成长观察与家校沟通，不构成医学诊断。",
        "risk_snapshot": {
            "risk_tier": tier,
            "risk_tier_label": _risk_label(tier),
            "mental_wellbeing_score": wellbeing,
            "flags": flags,
            "crisis_escalation": crisis,
            "crisis_reasons": crisis_reasons,
        },
        "key_findings": key_findings,
        "profile_interpretation": {
            "element_label": profile.get("element_label_zh", ""),
            "psychology_tag": profile.get("psychology_tag", ""),
            "psychology_summary": profile.get("psychology_summary", ""),
            "deep_psychology_labels": profile.get("deep_psychology_labels", []),
            "health_constitution_advice": profile.get("health_constitution_advice", []),
            "personality_tags": profile.get("personality_tags", []),
            "subject_strengths": profile.get("subject_strengths", []),
            "potential_development_directions": profile.get("potential_development_directions", []),
            "parenting_guidance": profile.get("parenting_guidance", []),
            "hands_on_and_self_discipline": profile.get("hands_on_and_self_discipline", {}),
            "emotion_and_friendship": profile.get("emotion_and_friendship", {}),
            "element_resolution": resolution_text,
        },
        "dimension_analysis": dimension_analysis,
        "growth_timeline": timeline,
        "action_plan": action_plan,
        "communication_script": {
            "for_parents": "建议使用“我们一起试试”的表述，减少“你应该”式指令，先稳定关系再谈改进。",
            "for_teachers": "优先给可执行的小目标和过程反馈，降低公开比较，强化阶段性进步体验。",
        },
    }
