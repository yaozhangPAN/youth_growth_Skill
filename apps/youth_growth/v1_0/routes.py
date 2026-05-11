"""Youth growth v1_0 API。"""
from __future__ import annotations

import json
from typing import Any

from flask import jsonify, request

from apps.youth_growth.v1_0 import blueprint
from util.skill_registry import get_registry
from util.youth_growth.curve_engine import get_yearly_curve
from util.youth_growth.profile_mapper import resolve_element
from util.youth_growth.questionnaire_template import QUESTIONNAIRE_TEMPLATE, SCORING_HELP


def _skill_invoke(payload: dict[str, Any]) -> dict[str, Any]:
    reg = get_registry()
    skill = reg.get("youth_growth_assessment")
    if skill is None:
        raise RuntimeError("youth_growth_assessment skill not registered")
    raw = skill.run(json.dumps(payload, ensure_ascii=False))
    return json.loads(raw)


@blueprint.post("/youth_growth/v1_0/assess")
def assess():
    data = request.get_json(silent=True) or {}
    questionnaire = data.get("questionnaire")
    if questionnaire is None or not isinstance(questionnaire, dict):
        return (
            jsonify(
                {
                    "code": 400,
                    "msg": "missing or invalid 'questionnaire' object",
                    "data": {},
                }
            ),
            400,
        )
    birth = data.get("birth")
    if birth is not None and not isinstance(birth, dict):
        return jsonify({"code": 400, "msg": "invalid 'birth' object", "data": {}}), 400

    payload = {
        "birth": birth,
        "questionnaire": questionnaire,
        "element_type": data.get("element_type") or data.get("dominant_element"),
    }
    try:
        out = _skill_invoke(payload)
    except Exception as exc:  # pragma: no cover
        return jsonify({"code": 500, "msg": str(exc), "data": {}}), 500
    return jsonify({"code": 200, "msg": "success!", "data": out}), 200


@blueprint.post("/youth_growth/v1_0/curve")
def curve_only():
    data = request.get_json(silent=True) or {}
    questionnaire = data.get("questionnaire") or {}
    birth = data.get("birth")
    element_override = data.get("element_type") or data.get("dominant_element")
    element, _resolution = resolve_element(
        birth=birth if isinstance(birth, dict) else None,
        questionnaire=questionnaire if isinstance(questionnaire, dict) else None,
        element_override=str(element_override).lower() if element_override else None,
    )
    curve = get_yearly_curve(element)
    return (
        jsonify(
            {
                "code": 200,
                "msg": "success!",
                "data": {
                    "element_key": element,
                    "years": curve,
                },
            }
        ),
        200,
    )


@blueprint.post("/youth_growth/v1_0/questionnaire/template")
def questionnaire_template():
    return (
        jsonify(
            {
                "code": 200,
                "msg": "success!",
                "data": {
                    "template": QUESTIONNAIRE_TEMPLATE,
                    "scoring": SCORING_HELP,
                },
            }
        ),
        200,
    )
