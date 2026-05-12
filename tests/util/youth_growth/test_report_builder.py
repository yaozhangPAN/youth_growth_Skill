"""Tests for report_builder helpers."""
from __future__ import annotations

from util.youth_growth.report_builder import (
    build_communication_script,
    build_detailed_report,
    build_recommended_actions,
)
from util.youth_growth.curve_engine import get_yearly_curve
from util.youth_growth.scoring import compute_scores


def test_build_recommended_actions_varies_with_questionnaire():
    scores = compute_scores(
        {
            "sdq_worried": 2,
            "sdq_unhappy": 2,
            "sdq_get_angry": 0,
            "sdq_think_before_act": 2,
            "sdq_restless": 2,
            "sdq_finish_tasks": 0,
            "sdq_has_good_friend": 0,
            "sdq_feel_isolated": 2,
            "sdq_help_others": 2,
            "sdq_kind_to_younger": 2,
        }
    )
    profile = {
        "parenting_guidance": [
            "养育建议 A。",
            "养育建议 B。",
            "养育建议 C。",
        ]
    }
    forecast = {"forecast_peak_years": [2028], "forecast_trough_years": [2026]}
    actions = build_recommended_actions(
        scores=scores,
        profile=profile,
        forecast_summary=forecast,
        questionnaire={"notes": "近期考试多"},
    )
    assert len(actions) >= 3
    assert any("心理健康观察分" in a for a in actions)
    assert any("流年预测" in a for a in actions)
    assert any("近期考试多" in a for a in actions)
    assert any("学业" in a or "补充说明侧重学业" in a for a in actions)


def test_build_recommended_actions_different_scores_change_opening():
    low = compute_scores(
        {
            "sdq_worried": 0,
            "sdq_unhappy": 0,
            "sdq_get_angry": 0,
            "sdq_think_before_act": 2,
            "sdq_restless": 0,
            "sdq_finish_tasks": 2,
            "sdq_has_good_friend": 2,
            "sdq_feel_isolated": 0,
            "sdq_help_others": 2,
            "sdq_kind_to_younger": 2,
        }
    )
    high = compute_scores(
        {
            "sdq_worried": 2,
            "sdq_unhappy": 2,
            "sdq_get_angry": 2,
            "sdq_think_before_act": 0,
            "sdq_restless": 2,
            "sdq_finish_tasks": 0,
            "sdq_has_good_friend": 0,
            "sdq_feel_isolated": 2,
            "sdq_help_others": 0,
            "sdq_kind_to_younger": 0,
        }
    )
    empty_profile: dict = {"parenting_guidance": []}
    fc: dict = {"forecast_peak_years": [], "forecast_trough_years": []}
    a_low = build_recommended_actions(
        scores=low, profile=empty_profile, forecast_summary=fc, questionnaire=None
    )
    a_high = build_recommended_actions(
        scores=high, profile=empty_profile, forecast_summary=fc, questionnaire=None
    )
    assert a_low[0] != a_high[0]


def _sample_profile() -> dict:
    return {
        "element_label_zh": "水系宝宝",
        "psychology_tag": "高内耗型智者 / 隐秘的胜负欲",
        "psychology_summary": "思维敏捷、内省深；压力下易思虑过度，需安全感与节奏管理。",
        "emotion_and_friendship": {"style": "同理强、压力下易退缩"},
    }


def test_communication_script_varies_by_tier_and_profile():
    low = compute_scores(
        {
            "sdq_worried": 0,
            "sdq_unhappy": 0,
            "sdq_get_angry": 0,
            "sdq_think_before_act": 2,
            "sdq_restless": 0,
            "sdq_finish_tasks": 2,
            "sdq_has_good_friend": 2,
            "sdq_feel_isolated": 0,
            "sdq_help_others": 2,
            "sdq_kind_to_younger": 2,
        }
    )
    high = compute_scores(
        {
            "sdq_worried": 2,
            "sdq_unhappy": 2,
            "sdq_get_angry": 2,
            "sdq_think_before_act": 0,
            "sdq_restless": 2,
            "sdq_finish_tasks": 0,
            "sdq_has_good_friend": 0,
            "sdq_feel_isolated": 2,
            "sdq_help_others": 0,
            "sdq_kind_to_younger": 0,
        }
    )
    p = _sample_profile()
    s_low = build_communication_script(scores=low, profile=p, crisis=False)
    s_high = build_communication_script(scores=high, profile=p, crisis=False)
    assert "从问卷整合的感受" in s_low["for_parents"]
    assert "相对平稳" in s_low["for_parents"] or "轻量倾听" in s_low["for_parents"]
    assert "内在承受的压力" in s_high["for_parents"] or "关系与安全" in s_high["for_parents"]
    assert s_low["for_parents"] != s_high["for_parents"]
    assert s_low["for_teachers"] != s_high["for_teachers"]
    assert "气质" in s_low["for_parents"] or "材料概述" in s_low["for_parents"]


def test_communication_script_crisis_branch():
    scores = compute_scores({})
    script = build_communication_script(scores=scores, profile={}, crisis=True)
    assert "安全" in script["for_parents"] or "专业" in script["for_parents"]
    assert "心理老师" in script["for_teachers"] or "转介" in script["for_teachers"]


def test_communication_script_crisis_includes_reasons_with_context():
    scores = compute_scores({})
    script = build_communication_script(
        scores=scores,
        profile={},
        crisis=True,
        report_context={"crisis_reasons": ["问卷出现自伤相关线索", "情绪极端波动"]},
    )
    assert "问卷出现自伤相关线索" in script["for_parents"]
    assert "情绪极端波动" in script["for_parents"]
    assert "问卷出现自伤相关线索" in script["for_teachers"]


def test_build_detailed_report_communication_uses_report_content():
    high = compute_scores(
        {
            "sdq_worried": 2,
            "sdq_unhappy": 2,
            "sdq_get_angry": 2,
            "sdq_think_before_act": 0,
            "sdq_restless": 2,
            "sdq_finish_tasks": 0,
            "sdq_has_good_friend": 0,
            "sdq_feel_isolated": 2,
            "sdq_help_others": 0,
            "sdq_kind_to_younger": 0,
        }
    )
    p = _sample_profile()
    p["subject_strengths"] = ["数理逻辑", "独立阅读"]
    curve = get_yearly_curve("water")
    report = build_detailed_report(
        scores=high,
        profile=p,
        curve=curve,
        peaks_troughs={"peak_years": [2031], "trough_years": [2026]},
        crisis=False,
        crisis_reasons=[],
        element_resolution="birth_day_stem",
        questionnaire={"notes": "最近考试压力很大，睡不着"},
    )
    parents = report["communication_script"]["for_parents"]
    teachers = report["communication_script"]["for_teachers"]

    assert "欲望与分心感上升" in parents or "内心浮躁" in parents
    assert "降低诱惑暴露" in parents or "分段学习" in parents
    assert "学业" in parents or "睡眠" in parents or "固定睡眠" in parents
    assert "数理逻辑" in parents or "独立阅读" in parents
    assert "报告要点：" in parents

    assert "专注力波动" in teachers
    assert "根据出生日期计算日干" in teachers

    sn = report.get("supplementary_notes_analysis") or {}
    assert sn.get("has_notes") is True
    assert "学业" in (sn.get("detected_themes") or []) or "作息与睡眠" in (sn.get("detected_themes") or [])
    assert any("补充说明" in x for x in (report.get("key_findings") or []))
    next_two = (report.get("action_plan") or {}).get("next_2_weeks") or []
    assert any("补充说明" in str(x) for x in next_two[:3])
