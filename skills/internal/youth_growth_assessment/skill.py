"""青少年成长评估 Skill：编排 util 层并输出 JSON 字符串。"""
from __future__ import annotations

import json
from typing import Any

from skills.base_skill import BaseSkill
from util.youth_growth.curve_engine import (
    build_forecast_curve,
    forecast_peaks_and_troughs,
    get_yearly_curve,
    peaks_and_troughs,
)
from util.youth_growth.profile_mapper import (
    ELEMENT_KEYS,
    analyze_birth_bazi,
    build_profile,
    resolve_element,
)
from util.youth_growth.report_builder import build_detailed_report, build_recommended_actions
from util.youth_growth.safety import crisis_from_questionnaire, escalation_message
from util.youth_growth.scoring import compute_scores


def _load_payload(user_input: str, kwargs: dict[str, Any]) -> dict[str, Any]:
    data: dict[str, Any] = {}
    if user_input and user_input.strip():
        try:
            parsed = json.loads(user_input)
            if isinstance(parsed, dict):
                data = parsed
        except json.JSONDecodeError:
            data = {"notes": user_input}
    for key in ("birth", "questionnaire", "element_type", "dominant_element"):
        if key in kwargs and kwargs[key] is not None:
            data[key] = kwargs[key]
    return data


def _crisis_recommended_actions() -> list[str]:
    return [
        escalation_message(),
        "在此之前，请确保当事人处于安全环境（移除危险物品），并由成年人陪同联系专业机构。",
    ]


class YouthGrowthAssessmentSkill(BaseSkill):
    name = "youth_growth_assessment"
    description = "青少年心理状态观察、五行倾向画像与年度成长曲线教育建议（非医疗诊断）"
    version = "1.0.0"

    def run(self, user_input: str, **kwargs: Any) -> str:
        payload = _load_payload(user_input, kwargs)
        birth = payload.get("birth")
        questionnaire = payload.get("questionnaire") or {}
        if not isinstance(questionnaire, dict):
            questionnaire = {}

        element_override = payload.get("element_type") or payload.get("dominant_element")
        eo_norm = None
        if isinstance(element_override, str) and element_override.strip().lower() in ELEMENT_KEYS:
            eo_norm = element_override.strip().lower()

        crisis, crisis_reasons = crisis_from_questionnaire(questionnaire)

        scores = compute_scores(questionnaire if isinstance(questionnaire, dict) else None)
        element, resolution = resolve_element(
            birth=birth if isinstance(birth, dict) else None,
            questionnaire=questionnaire if isinstance(questionnaire, dict) else None,
            element_override=eo_norm,
        )
        birth_bazi = analyze_birth_bazi(birth if isinstance(birth, dict) else None)
        profile = build_profile(element, birth_bazi=birth_bazi)
        curve = get_yearly_curve(element)
        pt = peaks_and_troughs(curve)
        forecast_curve = build_forecast_curve(curve)
        forecast_summary = forecast_peaks_and_troughs(forecast_curve)

        qdict = questionnaire if isinstance(questionnaire, dict) else {}
        recommended_actions: list[str] = (
            _crisis_recommended_actions()
            if crisis
            else build_recommended_actions(
                scores=scores,
                profile=profile,
                forecast_summary=forecast_summary,
                questionnaire=qdict,
            )
        )

        result: dict[str, Any] = {
            "meta": {
                "skill": self.name,
                "version": self.version,
                "element_resolution": resolution,
            },
            "safety_notice": (
                "本报告仅供教育与成长参考，不构成医学诊断、心理诊断或危机干预。"
                "如有身心不适或紧急情况，请寻求专业医疗与心理服务。"
            ),
            "crisis_escalation": crisis,
            "crisis_reasons": crisis_reasons,
            "mental_health_observation": scores,
            "profile": profile,
            "growth_curve": {
                "years": curve,
                "summary": pt,
                "forecast_curve": forecast_curve,
                "forecast_summary": forecast_summary,
            },
            "recommended_actions": recommended_actions,
        }
        if birth_bazi:
            result["meta"]["birth_bazi"] = birth_bazi
        result["detailed_report"] = build_detailed_report(
            scores=scores,
            profile=profile,
            curve=curve,
            peaks_troughs=pt,
            crisis=crisis,
            crisis_reasons=crisis_reasons,
            element_resolution=resolution,
            questionnaire=qdict,
        )

        if crisis:
            result["growth_curve"]["note"] = "危机路径下不强调年度曲线比较，请先处理安全与支持。"
        else:
            result["growth_curve"]["note"] = (
                "年度曲线为教育场景下的相对趋势提示，用于家校沟通与节奏安排。"
            )

        return json.dumps(result, ensure_ascii=False)
