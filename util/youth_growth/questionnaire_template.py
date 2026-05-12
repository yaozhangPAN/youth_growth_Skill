"""问卷模板与计分说明（与 scoring.normalize_questionnaire 对齐）。"""

from __future__ import annotations

QUESTIONNAIRE_TEMPLATE: dict = {
    "version": "1.0.0",
    "instrument": "sdq_friendly_short_v1",
    "scale": "SDQ 友好短表：0=不太符合，1=有一点符合，2=非常符合",
    "birth_fields": {
        "note": "与问卷并列传入 payload.birth；公历年月日必填，hour 为 0–23 的北京时间（东八区本地钟点）。",
        "hour_meaning": "用于历法四柱计算；不提供 hour 时仅用年月日三柱作结构参考，个性化会偏粗。",
    },
    "friendly_sdq_questions": [
        {"key": "sdq_worried", "label": "我经常担心或紧张。", "domain": "情绪症状"},
        {"key": "sdq_unhappy", "label": "我最近常常不开心。", "domain": "情绪症状"},
        {"key": "sdq_get_angry", "label": "我容易发脾气或和人顶撞。", "domain": "行为问题"},
        {"key": "sdq_think_before_act", "label": "我做事前会先想一想。", "domain": "行为问题（反向计分）"},
        {"key": "sdq_restless", "label": "我坐不太住，容易分心。", "domain": "多动/注意"},
        {"key": "sdq_finish_tasks", "label": "我能把事情做完，专注度还可以。", "domain": "多动/注意（反向计分）"},
        {"key": "sdq_has_good_friend", "label": "我至少有一个关系不错的朋友。", "domain": "同伴关系（反向计分）"},
        {"key": "sdq_feel_isolated", "label": "我常觉得被同学排斥或融不进去。", "domain": "同伴关系"},
        {"key": "sdq_help_others", "label": "我愿意主动帮助别人。", "domain": "亲社会行为"},
        {"key": "sdq_kind_to_younger", "label": "我会体谅别人、愿意照顾弱小。", "domain": "亲社会行为"},
    ],
    "safety_optional": [
        {
            "key": "self_harm_signal",
            "label": "近两周自伤念头频率（可选）",
            "scale": "1=从未，5=非常频繁",
            "meaning": "用于安全升级，不属于 SDQ 本体",
        },
    ],
    "compatibility_notes": [
        "系统会自动把 SDQ 维度映射到内部风险评估维度。",
        "若仍传入旧版 1-5 维度字段，系统继续兼容。",
    ],
    "free_text": [
        {
            "key": "notes",
            "label": "补充说明（可选）",
            "meaning": "会被安全扫描；请勿用于替代专业求助",
        }
    ],
}

SCORING_HELP = {
    "mental_wellbeing_score": "0–100，基于 SDQ 困难总分与亲社会维度映射（教育观察指标，非诊断）",
    "risk_tier": "low / medium / high，基于 wellbeing 分数与安全信号阈值",
}
