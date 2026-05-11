"""青少年成长：问卷评分与风险分层。"""

from __future__ import annotations

from typing import Any

# 维度说明：1–5，数值越高表示该维度「困扰/压力」越大（正向项除外）
# sleep_quality / social_support / study_engagement：越高越好（睡眠好、支持足、投入高）
DEFAULT_DIMENSION_KEYS = (
    "emotion_dysregulation",  # 情绪调节困难程度
    "stress_level",  # 压力感
    "social_isolation",  # 孤独/被排斥感
    "academic_pressure",  # 学业压力感
    "sleep_quality",  # 睡眠质量（越高越好，计算时反转）
    "attention_focus",  # 专注困难程度
    "mood_low_energy",  # 低落/无力感
    "risk_behaviors",  # 冒险/冲动行为倾向
)

# 自杀/自伤相关：单独高分触发危机路径
SELF_HARM_SIGNAL = "self_harm_signal"

SDQ_FRIENDLY_ITEMS: dict[str, dict[str, Any]] = {
    "sdq_worried": {"domain": "emotional", "reverse": False},
    "sdq_unhappy": {"domain": "emotional", "reverse": False},
    "sdq_get_angry": {"domain": "conduct", "reverse": False},
    "sdq_think_before_act": {"domain": "conduct", "reverse": True},
    "sdq_restless": {"domain": "hyperactivity", "reverse": False},
    "sdq_finish_tasks": {"domain": "hyperactivity", "reverse": True},
    "sdq_has_good_friend": {"domain": "peer", "reverse": True},
    "sdq_feel_isolated": {"domain": "peer", "reverse": False},
    "sdq_help_others": {"domain": "prosocial", "reverse": False},
    "sdq_kind_to_younger": {"domain": "prosocial", "reverse": False},
}

SDQ_DOMAINS = ("emotional", "conduct", "hyperactivity", "peer", "prosocial")


def _clamp_int(v: Any, default: int = 3) -> int:
    try:
        x = int(v)
    except (TypeError, ValueError):
        return default
    return max(1, min(5, x))


def _clamp_sdq(v: Any, default: int = 1) -> int:
    """
    SDQ 友好问卷采用 0-2 三点评分：
    0=不太符合，1=有一点符合，2=非常符合
    """
    try:
        x = int(v)
    except (TypeError, ValueError):
        return default
    return max(0, min(2, x))


def _has_sdq_answers(raw: dict[str, Any]) -> bool:
    return any(k in raw for k in SDQ_FRIENDLY_ITEMS)


def _score_sdq_short(raw: dict[str, Any]) -> dict[str, Any]:
    domain_scores = {k: 0 for k in SDQ_DOMAINS}
    answers: dict[str, int] = {}
    for key, meta in SDQ_FRIENDLY_ITEMS.items():
        raw_value = _clamp_sdq(raw.get(key), default=1)
        answers[key] = raw_value
        scored = 2 - raw_value if bool(meta.get("reverse")) else raw_value
        domain = str(meta.get("domain"))
        domain_scores[domain] += scored

    total_difficulties = (
        domain_scores["emotional"]
        + domain_scores["conduct"]
        + domain_scores["hyperactivity"]
        + domain_scores["peer"]
    )
    return {
        "answers": answers,
        "domain_scores": domain_scores,
        "total_difficulties": total_difficulties,
        "prosocial_score": domain_scores["prosocial"],
    }


def _to_1_5(value_0_4: int) -> int:
    return max(1, min(5, int(value_0_4) + 1))


def _sdq_to_legacy_dimensions(sdq: dict[str, int], raw: dict[str, Any]) -> dict[str, int]:
    emotional = int(sdq.get("emotional", 2))
    conduct = int(sdq.get("conduct", 2))
    hyper = int(sdq.get("hyperactivity", 2))
    peer = int(sdq.get("peer", 2))

    # 将 SDQ 领域分（0-4）映射到现有 1-5 维度，保持兼容输出结构
    stress_proxy = round((emotional + peer + hyper) / 3.0)
    mood_proxy = round((emotional + peer) / 2.0)
    sleep_proxy = 4 - round((emotional + hyper) / 2.0)

    out = {
        "emotion_dysregulation": _to_1_5(round((emotional + conduct) / 2.0)),
        "stress_level": _to_1_5(stress_proxy),
        "social_isolation": _to_1_5(peer),
        "academic_pressure": _to_1_5(round((hyper + emotional) / 2.0)),
        "sleep_quality": _to_1_5(sleep_proxy),
        "attention_focus": _to_1_5(hyper),
        "mood_low_energy": _to_1_5(mood_proxy),
        "risk_behaviors": _to_1_5(conduct),
    }
    if SELF_HARM_SIGNAL in raw:
        out[SELF_HARM_SIGNAL] = _clamp_int(raw.get(SELF_HARM_SIGNAL), default=1)
    return out


def normalize_questionnaire(raw: dict[str, Any] | None) -> dict[str, int]:
    """补全默认并约束在 1–5。"""
    if not raw:
        raw = {}
    out: dict[str, int] = {}
    for key in DEFAULT_DIMENSION_KEYS:
        out[key] = _clamp_int(raw.get(key), default=3)
    # 可选：自伤念头单独字段（1-5，越高越频繁）
    if SELF_HARM_SIGNAL in raw:
        out[SELF_HARM_SIGNAL] = _clamp_int(raw.get(SELF_HARM_SIGNAL), default=1)
    return out


def _apply_self_harm_adjustment(score: float, dimensions: dict[str, int]) -> float:
    if SELF_HARM_SIGNAL in dimensions:
        sh = dimensions[SELF_HARM_SIGNAL]
        if sh >= 4:
            score -= 35
        elif sh >= 3:
            score -= 20
        elif sh >= 2:
            score -= 8
    return score


def compute_mental_wellbeing_score(dimensions: dict[str, int]) -> float:
    """
    返回 0–100，越高表示整体心理状态越稳定、适应越好（教育观察用，非诊断）。
    基于维度加权：压力类越高扣越多；sleep_quality 越高加分越多。
    """
    # 反转「越高越好」的项
    sleep = dimensions.get("sleep_quality", 3)
    sleep_contrib = (sleep - 1) / 4.0 * 100  # 1->0, 5->100

    stress_like = (
        dimensions.get("emotion_dysregulation", 3)
        + dimensions.get("stress_level", 3)
        + dimensions.get("social_isolation", 3)
        + dimensions.get("academic_pressure", 3)
        + dimensions.get("attention_focus", 3)
        + dimensions.get("mood_low_energy", 3)
        + dimensions.get("risk_behaviors", 3)
    ) / 7.0

    # stress_like 1->最好, 5->最差；映射到 0-100 分损失
    stress_penalty = (stress_like - 1) / 4.0 * 70

    base = 100.0 - stress_penalty
    # 睡眠占一定正向权重
    score = 0.65 * base + 0.35 * sleep_contrib
    # 自伤信号极强时压低分数（仍非医学判定）
    score = _apply_self_harm_adjustment(score, dimensions)
    return max(0.0, min(100.0, round(score, 1)))


def compute_mental_wellbeing_score_sdq(sdq_summary: dict[str, Any], dimensions: dict[str, int]) -> float:
    total_diff = float(sdq_summary.get("total_difficulties", 8))  # 0-16
    prosocial = float(sdq_summary.get("prosocial_score", 2))  # 0-4
    difficulties_component = (1.0 - total_diff / 16.0) * 85.0
    prosocial_component = (prosocial / 4.0) * 15.0
    score = difficulties_component + prosocial_component
    score = _apply_self_harm_adjustment(score, dimensions)
    return max(0.0, min(100.0, round(score, 1)))


def risk_tier_from_score(wellbeing: float) -> str:
    if wellbeing >= 70:
        return "low"
    if wellbeing >= 45:
        return "medium"
    return "high"


def summarize_flags(dimensions: dict[str, int]) -> list[str]:
    flags: list[str] = []
    if dimensions.get("stress_level", 0) >= 4:
        flags.append("elevated_stress")
    if dimensions.get("sleep_quality", 5) <= 2:
        flags.append("poor_sleep")
    if dimensions.get("social_isolation", 0) >= 4:
        flags.append("social_distress")
    if dimensions.get("mood_low_energy", 0) >= 4:
        flags.append("low_mood_energy")
    if dimensions.get(SELF_HARM_SIGNAL, 0) >= 3:
        flags.append("self_harm_concern")
    return flags


def summarize_flags_sdq(sdq_domain_scores: dict[str, int]) -> list[str]:
    flags: list[str] = []
    if sdq_domain_scores.get("emotional", 0) >= 3:
        flags.append("sdq_emotional_distress")
    if sdq_domain_scores.get("hyperactivity", 0) >= 3:
        flags.append("sdq_attention_hyperactivity")
    if sdq_domain_scores.get("peer", 0) >= 3:
        flags.append("sdq_peer_relation_strain")
    if sdq_domain_scores.get("conduct", 0) >= 3:
        flags.append("sdq_conduct_regulation_risk")
    if sdq_domain_scores.get("prosocial", 4) <= 1:
        flags.append("sdq_low_prosocial_behavior")
    return flags


def compute_scores(questionnaire: dict[str, Any] | None) -> dict[str, Any]:
    raw = questionnaire or {}
    if isinstance(raw, dict) and _has_sdq_answers(raw):
        sdq_summary = _score_sdq_short(raw)
        domain_scores = sdq_summary["domain_scores"]
        dims = _sdq_to_legacy_dimensions(domain_scores, raw)
        wellbeing = compute_mental_wellbeing_score_sdq(sdq_summary, dims)
        tier = risk_tier_from_score(wellbeing)
        merged_flags = list(dict.fromkeys(summarize_flags(dims) + summarize_flags_sdq(domain_scores)))
        return {
            "dimensions": dims,
            "mental_wellbeing_score": wellbeing,
            "risk_tier": tier,
            "flags": merged_flags,
            "instrument": "sdq_friendly_short_v1",
            "sdq": {
                "answer_scale": "0-2",
                "question_count": len(SDQ_FRIENDLY_ITEMS),
                "domain_scores": domain_scores,
                "total_difficulties": sdq_summary["total_difficulties"],
                "prosocial_score": sdq_summary["prosocial_score"],
            },
        }

    dims = normalize_questionnaire(raw if isinstance(raw, dict) else None)
    wellbeing = compute_mental_wellbeing_score(dims)
    tier = risk_tier_from_score(wellbeing)
    return {
        "dimensions": dims,
        "mental_wellbeing_score": wellbeing,
        "risk_tier": tier,
        "flags": summarize_flags(dims),
        "instrument": "legacy_dimension_v1",
    }
