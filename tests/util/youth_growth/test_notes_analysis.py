"""Tests for supplementary notes analysis."""
from __future__ import annotations

from util.youth_growth.notes_analysis import analyze_supplementary_notes


def test_analyze_notes_empty():
    r = analyze_supplementary_notes("")
    assert r["has_notes"] is False
    assert r["emphasis_dimension_keys"] == []


def test_analyze_notes_academic_and_emphasis():
    dims = {
        "emotion_dysregulation": 2,
        "stress_level": 3,
        "social_isolation": 2,
        "academic_pressure": 4,
        "sleep_quality": 4,
        "attention_focus": 2,
        "mood_low_energy": 2,
        "risk_behaviors": 2,
    }
    r = analyze_supplementary_notes("最近考试很多，压力大", dimensions=dims)
    assert r["has_notes"] is True
    assert "学业与任务节奏" in (r.get("detected_themes") or [])
    assert "academic_pressure" in (r.get("emphasis_dimension_keys") or [])


def test_analyze_notes_no_theme_still_has_summary():
    r = analyze_supplementary_notes("一些说不清的感受", dimensions=None)
    assert r["has_notes"] is True
    assert r["adjustment_summary"]
    assert not r["detected_themes"]
