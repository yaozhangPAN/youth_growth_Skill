"""Youth growth assessment skill tests."""
from __future__ import annotations

import json

import pytest

from skills.internal.youth_growth_assessment.skill import YouthGrowthAssessmentSkill


@pytest.fixture
def skill():
    return YouthGrowthAssessmentSkill()


def test_run_returns_json_with_expected_keys(skill):
    payload = {
        "birth": {"year": 2012, "month": 6, "day": 15},
        "questionnaire": {
            "emotion_dysregulation": 2,
            "stress_level": 3,
            "social_isolation": 2,
            "academic_pressure": 3,
            "sleep_quality": 4,
            "attention_focus": 2,
            "mood_low_energy": 2,
            "risk_behaviors": 2,
        },
    }
    out = json.loads(skill.run(json.dumps(payload)))
    assert out["meta"]["skill"] == "youth_growth_assessment"
    assert "mental_health_observation" in out
    assert "growth_curve" in out
    assert out["crisis_escalation"] is False


def test_crisis_keyword_escalation(skill):
    payload = {
        "questionnaire": {
            "emotion_dysregulation": 2,
            "stress_level": 3,
            "social_isolation": 2,
            "academic_pressure": 3,
            "sleep_quality": 4,
            "attention_focus": 2,
            "mood_low_energy": 2,
            "risk_behaviors": 2,
            "notes": "我最近不想活了",
        }
    }
    out = json.loads(skill.run(json.dumps(payload)))
    assert out["crisis_escalation"] is True
    assert out["growth_curve"]["note"].startswith("危机")


def test_element_override(skill):
    payload = {
        "questionnaire": {"stress_level": 3, "sleep_quality": 4},
        "element_type": "fire",
    }
    out = json.loads(skill.run(json.dumps(payload)))
    assert out["profile"]["element_key"] == "fire"
    assert out["meta"]["element_resolution"] == "explicit_override"
