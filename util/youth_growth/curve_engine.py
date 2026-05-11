"""年度成长曲线引擎：2026–2031 静态矩阵（来自 reference 文档的结构化摘录）。"""
from __future__ import annotations

from typing import Any

YEARS = tuple(range(2026, 2032))

# 五星制简化：学习专心度、身心健康提示强度、快乐指数（越高越好）
# 每项 1-5；文档中的定性描述压缩为 short / guidance / concern

_CURVES: dict[str, list[dict[str, Any]]] = {
    "water": [
        {
            "year": 2026,
            "pillar_tag": "水火交战",
            "psych_state": "欲望与分心感上升，内心浮躁，易贪玩与内耗。",
            "learning_focus": 2,
            "wellbeing_hint": 2,
            "joy_index": 4,
            "concern": "专注力波动；用眼与作息。",
            "guidance": "降低诱惑暴露，分段学习与规律作息。",
        },
        {
            "year": 2027,
            "pillar_tag": "财杀相生",
            "psych_state": "压力内化，对规则敏感，不服输感增强。",
            "learning_focus": 4,
            "wellbeing_hint": 3,
            "joy_index": 4,
            "concern": "脾胃与泌尿系统易感不适（身心联动提示）。",
            "guidance": "把压力拆成小目标；强化睡眠与饮食节律。",
        },
        {
            "year": 2028,
            "pillar_tag": "金水相生",
            "psych_state": "底气回升，思维灵动，理科投入感增强。",
            "learning_focus": 5,
            "wellbeing_hint": 4,
            "joy_index": 5,
            "concern": "久坐与作息失衡。",
            "guidance": "保持运动与学习交替，避免熬夜刷题。",
        },
        {
            "year": 2029,
            "pillar_tag": "杀印相生",
            "psych_state": "责任感与自律上升，承压能力提升。",
            "learning_focus": 5,
            "wellbeing_hint": 4,
            "joy_index": 4,
            "concern": "用脑过度致浅睡。",
            "guidance": "睡前放松流程；适度降低夜间刺激性屏幕使用。",
        },
        {
            "year": 2030,
            "pillar_tag": "正印制伤",
            "psych_state": "思维趋深，偏好体系化与抽象理解。",
            "learning_focus": 4,
            "wellbeing_hint": 4,
            "joy_index": 4,
            "concern": "皮肤干燥与补水不足（身心提示）。",
            "guidance": "竞赛备考期分段冲刺；保留户外与同伴互动。",
        },
        {
            "year": 2031,
            "pillar_tag": "印比相助",
            "psych_state": "思维敏捷度峰值期，合作与分享需刻意练习。",
            "learning_focus": 4,
            "wellbeing_hint": 5,
            "joy_index": 4,
            "concern": "粗心与社交疲劳。",
            "guidance": "清单化与复盘；控制课外负荷。",
        },
    ],
    "metal": [
        {
            "year": 2026,
            "pillar_tag": "烈火炼金",
            "psych_state": "高压感与危机感上升，易对权威抵触或自卑。",
            "learning_focus": 4,
            "wellbeing_hint": 2,
            "joy_index": 4,
            "concern": "呼吸道、鼻炎、牙齿骨骼外伤提示。",
            "guidance": "家长降低羞辱式批评；用『细节肯定』替代笼统责备。",
        },
        {
            "year": 2027,
            "pillar_tag": "官印相生",
            "psych_state": "自尊与规矩感增强，愿意承担责任。",
            "learning_focus": 5,
            "wellbeing_hint": 4,
            "joy_index": 5,
            "concern": "肠道与皮肤偏燥。",
            "guidance": "适合班干部与结构化任务；饮水与膳食纤维。",
        },
        {
            "year": 2028,
            "pillar_tag": "比劫当令",
            "psych_state": "好胜与冒险感强，易自负或急躁。",
            "learning_focus": 3,
            "wellbeing_hint": 4,
            "joy_index": 4,
            "concern": "运动外伤提示。",
            "guidance": "竞技类出口；作业放慢审题步骤。",
        },
        {
            "year": 2029,
            "pillar_tag": "印生比劫",
            "psych_state": "固执与自我意识增强，倾听变难。",
            "learning_focus": 4,
            "wellbeing_hint": 3,
            "joy_index": 3,
            "concern": "呼吸道敏感与小外伤。",
            "guidance": "同伴调解与冲突复盘；避免『赢辩论输了关系』。",
        },
        {
            "year": 2030,
            "pillar_tag": "枭神夺食",
            "psych_state": "抱怨与敏感上升，创造力受压感。",
            "learning_focus": 3,
            "wellbeing_hint": 3,
            "joy_index": 3,
            "concern": "睡眠与消化波动。",
            "guidance": "兴趣出口（音乐/体育）；识别厌学早期信号。",
        },
        {
            "year": 2031,
            "pillar_tag": "食神泄秀",
            "psych_state": "逻辑与记忆峰值期，表达趋于利落。",
            "learning_focus": 5,
            "wellbeing_hint": 5,
            "joy_index": 5,
            "concern": "恃才傲物与人际孤立。",
            "guidance": "团队协作任务；教授倾听式反馈。",
        },
    ],
    "earth": [
        {
            "year": 2026,
            "pillar_tag": "印星极旺",
            "psych_state": "安全感上升但也易依赖舒适区。",
            "learning_focus": 5,
            "wellbeing_hint": 3,
            "joy_index": 4,
            "concern": "脾胃积热与口腔不适提示。",
            "guidance": "背诵类优势期；建立『适度挑战』阶梯。",
        },
        {
            "year": 2027,
            "pillar_tag": "印比生扶",
            "psych_state": "包容稳定，同伴关系缓和。",
            "learning_focus": 4,
            "wellbeing_hint": 4,
            "joy_index": 4,
            "concern": "运动不足与体态。",
            "guidance": "固定运动时段；小组合作学习。",
        },
        {
            "year": 2028,
            "pillar_tag": "食神吐秀",
            "psych_state": "表达欲上升，动手与实验兴趣强。",
            "learning_focus": 5,
            "wellbeing_hint": 4,
            "joy_index": 5,
            "concern": "精力消耗大，劳逸结合。",
            "guidance": "机器人/实验项目式学习；竞赛节奏循序渐进。",
        },
        {
            "year": 2029,
            "pillar_tag": "伤官生财",
            "psych_state": "反叛与创新并存，挑战权威答案。",
            "learning_focus": 5,
            "wellbeing_hint": 3,
            "joy_index": 5,
            "concern": "肠道敏感提示。",
            "guidance": "给『可控选择权』；编程与逻辑项目疏导能量。",
        },
        {
            "year": 2030,
            "pillar_tag": "比劫食伤",
            "psych_state": "竞争与合作并存，策略性增强。",
            "learning_focus": 4,
            "wellbeing_hint": 4,
            "joy_index": 4,
            "concern": "泌尿与皮肤干燥提示。",
            "guidance": "文理并进的项目制任务；聚焦核心兴趣。",
        },
        {
            "year": 2031,
            "pillar_tag": "食伤生财",
            "psych_state": "目标感强，应用导向提升。",
            "learning_focus": 4,
            "wellbeing_hint": 4,
            "joy_index": 4,
            "concern": "兴趣过多导致分散。",
            "guidance": "精简课外班；强调产出与复盘。",
        },
    ],
    "wood": [
        {
            "year": 2026,
            "pillar_tag": "木火通明",
            "psych_state": "表现欲强，创造力与外放情绪上升。",
            "learning_focus": 5,
            "wellbeing_hint": 2,
            "joy_index": 5,
            "concern": "失眠、烦躁、用眼过度提示。",
            "guidance": "演讲/艺术出口；情绪命名与暂停技巧。",
        },
        {
            "year": 2027,
            "pillar_tag": "伤官生财",
            "psych_state": "思维跳跃，渴望认同，注意力易分散。",
            "learning_focus": 4,
            "wellbeing_hint": 3,
            "joy_index": 4,
            "concern": "用眼与作息。",
            "guidance": "项目式学习；基础作业分段计时。",
        },
        {
            "year": 2028,
            "pillar_tag": "七杀攻身",
            "psych_state": "高压与畏惧感上升，易退缩或自卑。",
            "learning_focus": 2,
            "wellbeing_hint": 2,
            "joy_index": 2,
            "concern": "外伤与筋骨提示（运动防护）。",
            "guidance": "降低羞辱式评价；拆任务与陪伴式启动。",
        },
        {
            "year": 2029,
            "pillar_tag": "财生官杀",
            "psych_state": "逐步接受规则，务实感增强。",
            "learning_focus": 4,
            "wellbeing_hint": 3,
            "joy_index": 4,
            "concern": "肩颈紧张与情绪性胃痛提示。",
            "guidance": "理科补齐短板的脚手架练习；规律运动。",
        },
        {
            "year": 2030,
            "pillar_tag": "杀印相配",
            "psych_state": "韧性回升，责任感与自信修复。",
            "learning_focus": 5,
            "wellbeing_hint": 4,
            "joy_index": 5,
            "concern": "考试焦虑提示（身心联动）。",
            "guidance": "模拟考节奏训练；睡眠优先策略。",
        },
        {
            "year": 2031,
            "pillar_tag": "水生木印",
            "psych_state": "安静思考与深度阅读窗口期。",
            "learning_focus": 5,
            "wellbeing_hint": 5,
            "joy_index": 5,
            "concern": "动力偏低与拖延提示。",
            "guidance": "行动触发清单；同伴共读与输出。",
        },
    ],
    "fire": [
        {
            "year": 2026,
            "pillar_tag": "比劫羊刃",
            "psych_state": "冲动与竞争感强，课堂静坐困难。",
            "learning_focus": 2,
            "wellbeing_hint": 2,
            "joy_index": 4,
            "concern": "心血管负荷与发热提示（剧烈活动时留意）。",
            "guidance": "竞技体育与团队规则；分段学习与即时反馈。",
        },
        {
            "year": 2027,
            "pillar_tag": "比劫泄秀",
            "psych_state": "热心外向，协作意愿强但收尾弱。",
            "learning_focus": 4,
            "wellbeing_hint": 3,
            "joy_index": 4,
            "concern": "免疫力短时波动提示。",
            "guidance": "小组讨论带动学习；刻意练习『收尾复盘』。",
        },
        {
            "year": 2028,
            "pillar_tag": "偏财当令",
            "psych_state": "目标感与功利动机上升，更能忍受枯燥练习。",
            "learning_focus": 4,
            "wellbeing_hint": 4,
            "joy_index": 4,
            "concern": "干咳嗓音与肠道提示。",
            "guidance": "理化思维训练；奖励规则透明化。",
        },
        {
            "year": 2029,
            "pillar_tag": "伤官生财",
            "psych_state": "反叛与创新巅峰，应试表现可能两极化。",
            "learning_focus": 5,
            "wellbeing_hint": 3,
            "joy_index": 5,
            "concern": "晚睡与神经兴奋。",
            "guidance": "跨学科项目；保留睡眠红线。",
        },
        {
            "year": 2030,
            "pillar_tag": "食伤入库",
            "psych_state": "外放收敛，反思加深，体系化提升。",
            "learning_focus": 4,
            "wellbeing_hint": 4,
            "joy_index": 4,
            "concern": "室内久坐与缺氧感提示。",
            "guidance": "深度阅读与数理闭环；间歇户外活动。",
        },
        {
            "year": 2031,
            "pillar_tag": "官杀压身",
            "psych_state": "规则与选拔压力上升，自律考验增强。",
            "learning_focus": 4,
            "wellbeing_hint": 3,
            "joy_index": 3,
            "concern": "视力与紧张性心悸提示。",
            "guidance": "考前预案与放松训练；降低『一次性定论』语言。",
        },
    ],
}

_FORECAST_BASELINES: dict[str, dict[str, float]] = {
    "water": {
        "emotion_stability_index": 3.1,
        "social_adaptability_index": 3.0,
        "self_discipline_index": 3.3,
        "hands_on_action_index": 3.2,
        "health_constitution_index": 3.1,
    },
    "metal": {
        "emotion_stability_index": 3.0,
        "social_adaptability_index": 2.9,
        "self_discipline_index": 3.8,
        "hands_on_action_index": 3.4,
        "health_constitution_index": 3.0,
    },
    "earth": {
        "emotion_stability_index": 3.4,
        "social_adaptability_index": 3.2,
        "self_discipline_index": 3.4,
        "hands_on_action_index": 3.6,
        "health_constitution_index": 3.3,
    },
    "wood": {
        "emotion_stability_index": 2.9,
        "social_adaptability_index": 3.5,
        "self_discipline_index": 3.0,
        "hands_on_action_index": 3.8,
        "health_constitution_index": 3.0,
    },
    "fire": {
        "emotion_stability_index": 2.8,
        "social_adaptability_index": 3.7,
        "self_discipline_index": 2.9,
        "hands_on_action_index": 3.6,
        "health_constitution_index": 2.9,
    },
}


def _clamp_1_5(value: float) -> float:
    return max(1.0, min(5.0, round(value, 2)))


def _enrich_row_with_forecast(element_key: str, row: dict[str, Any]) -> dict[str, Any]:
    base = _FORECAST_BASELINES.get(element_key, _FORECAST_BASELINES["earth"])
    learning_focus = float(row.get("learning_focus", 3))
    wellbeing_hint = float(row.get("wellbeing_hint", 3))
    joy_index = float(row.get("joy_index", 3))

    emotion = _clamp_1_5(base["emotion_stability_index"] + 0.45 * (wellbeing_hint - 3) + 0.15 * (joy_index - 3))
    social = _clamp_1_5(base["social_adaptability_index"] + 0.35 * (joy_index - 3) + 0.15 * (wellbeing_hint - 3))
    discipline = _clamp_1_5(base["self_discipline_index"] + 0.5 * (learning_focus - 3) + 0.1 * (wellbeing_hint - 3))
    hands_on = _clamp_1_5(base["hands_on_action_index"] + 0.3 * (learning_focus - 3) + 0.25 * (joy_index - 3))
    health = _clamp_1_5(base["health_constitution_index"] + 0.55 * (wellbeing_hint - 3))
    overall = _clamp_1_5(0.3 * learning_focus + 0.25 * wellbeing_hint + 0.2 * joy_index + 0.25 * health)

    out = dict(row)
    out["forecast_indices"] = {
        "overall_index": overall,
        "emotion_stability_index": emotion,
        "social_adaptability_index": social,
        "self_discipline_index": discipline,
        "hands_on_action_index": hands_on,
        "health_constitution_index": health,
    }
    return out


def build_forecast_curve(curve: list[dict[str, Any]]) -> list[dict[str, Any]]:
    points: list[dict[str, Any]] = []
    for row in curve:
        metrics = row.get("forecast_indices", {})
        points.append(
            {
                "year": int(row.get("year", 0)),
                "overall_index": float(metrics.get("overall_index", 3)),
                "learning_focus_index": float(row.get("learning_focus", 3)),
                "emotion_stability_index": float(metrics.get("emotion_stability_index", 3)),
                "social_adaptability_index": float(metrics.get("social_adaptability_index", 3)),
                "self_discipline_index": float(metrics.get("self_discipline_index", 3)),
                "hands_on_action_index": float(metrics.get("hands_on_action_index", 3)),
                "health_constitution_index": float(metrics.get("health_constitution_index", 3)),
            }
        )
    return points


def forecast_peaks_and_troughs(forecast_curve: list[dict[str, Any]]) -> dict[str, list[int]]:
    if not forecast_curve:
        return {"forecast_peak_years": [], "forecast_trough_years": []}
    scores = [float(item.get("overall_index", 3)) for item in forecast_curve]
    years = [int(item.get("year", 0)) for item in forecast_curve]
    mi, ma = min(scores), max(scores)
    troughs = [years[i] for i, v in enumerate(scores) if v == mi]
    peaks = [years[i] for i, v in enumerate(scores) if v == ma]
    return {"forecast_peak_years": peaks, "forecast_trough_years": troughs}


def get_yearly_curve(element_key: str) -> list[dict[str, Any]]:
    key = element_key if element_key in _CURVES else "earth"
    # 返回拷贝避免上游修改，并补充流年预测指标曲线数据
    return [_enrich_row_with_forecast(key, row) for row in _CURVES[key]]


def peaks_and_troughs(curve: list[dict[str, Any]]) -> dict[str, list[int]]:
    """根据 learning_focus 找相对低谷与高峰年份（演示用）。"""
    if not curve:
        return {"trough_years": [], "peak_years": []}
    lf = [int(r.get("learning_focus", 3)) for r in curve]
    years = [int(r["year"]) for r in curve]
    mi, ma = min(lf), max(lf)
    troughs = [years[i] for i, v in enumerate(lf) if v == mi]
    peaks = [years[i] for i, v in enumerate(lf) if v == ma]
    return {"trough_years": troughs, "peak_years": peaks}
