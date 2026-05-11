"""Youth growth API tests."""
from __future__ import annotations

import json


def test_health(client):
    r = client.post("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_assess_missing_questionnaire(client):
    r = client.post("/youth_growth/v1_0/assess", json={})
    assert r.status_code == 400


def test_assess_success(client):
    body = {
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
    r = client.post("/youth_growth/v1_0/assess", json=body)
    assert r.status_code == 200
    data = r.get_json()
    assert data["code"] == 200
    assert "mental_health_observation" in data["data"]


def test_questionnaire_template(client):
    r = client.post("/youth_growth/v1_0/questionnaire/template", json={})
    assert r.status_code == 200
    assert "template" in r.get_json()["data"]


def test_curve(client):
    r = client.post(
        "/youth_growth/v1_0/curve",
        json={"birth": {"year": 2012, "month": 6, "day": 15}, "questionnaire": {}},
    )
    assert r.status_code == 200
    assert r.get_json()["data"]["years"]


def test_skills_list(client):
    r = client.post("/skills/v1_0/list", json={})
    assert r.status_code == 200
    names = [s["name"] for s in r.get_json()["data"]["skills"]]
    assert "youth_growth_assessment" in names


def test_skills_invoke(client):
    payload = {
        "input": json.dumps(
            {
                "questionnaire": {
                    "emotion_dysregulation": 2,
                    "stress_level": 3,
                    "social_isolation": 2,
                    "academic_pressure": 3,
                    "sleep_quality": 4,
                    "attention_focus": 2,
                    "mood_low_energy": 2,
                    "risk_behaviors": 2,
                }
            }
        )
    }
    r = client.post("/skills/v1_0/youth_growth_assessment/invoke", json=payload)
    assert r.status_code == 200
    assert r.get_json()["data"]["output"]["profile"]
