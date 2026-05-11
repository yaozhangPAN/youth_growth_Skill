"""util youth_growth scoring tests."""
from __future__ import annotations

from util.youth_growth.scoring import (
    compute_scores,
    risk_tier_from_score,
    summarize_flags,
)


def test_wellbeing_higher_when_stress_low():
    good = {
        "emotion_dysregulation": 1,
        "stress_level": 1,
        "social_isolation": 1,
        "academic_pressure": 1,
        "sleep_quality": 5,
        "attention_focus": 1,
        "mood_low_energy": 1,
        "risk_behaviors": 1,
    }
    bad = dict(good)
    bad.update(
        {
            "stress_level": 5,
            "sleep_quality": 1,
            "mood_low_energy": 5,
        }
    )
    assert compute_scores(good)["mental_wellbeing_score"] > compute_scores(bad)["mental_wellbeing_score"]


def test_self_harm_signal_lowers_score():
    base = {"stress_level": 3, "sleep_quality": 3}
    out1 = compute_scores(base)
    base2 = dict(base)
    base2["self_harm_signal"] = 4
    out2 = compute_scores(base2)
    assert out2["mental_wellbeing_score"] < out1["mental_wellbeing_score"]
    assert "self_harm_concern" in out2["flags"]


def test_risk_tier_thresholds():
    assert risk_tier_from_score(75) == "low"
    assert risk_tier_from_score(55) == "medium"
    assert risk_tier_from_score(30) == "high"


def test_summarize_flags():
    q = {"stress_level": 5, "sleep_quality": 1, "social_isolation": 5}
    flags = summarize_flags(q)
    assert "elevated_stress" in flags
    assert "poor_sleep" in flags
    assert "social_distress" in flags
