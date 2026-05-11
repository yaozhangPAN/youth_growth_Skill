"""Tests for report_builder helpers."""
from __future__ import annotations

from util.youth_growth.report_builder import build_recommended_actions
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
