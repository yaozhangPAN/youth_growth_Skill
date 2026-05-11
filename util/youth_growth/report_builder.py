"""Detailed report builder for education-facing narratives."""
from __future__ import annotations

from typing import Any


_DIMENSION_META: dict[str, dict[str, Any]] = {
    "emotion_dysregulation": {
        "label": "情绪调节困难",
        "positive": False,
        "high": "情绪波动偏明显，建议减少对抗式沟通并建立情绪降温流程。",
        "mid": "情绪调节有波动，适合用固定作息和情绪命名练习稳定节奏。",
        "low": "情绪总体较稳，可继续保持表达与复盘习惯。",
    },
    "stress_level": {
        "label": "压力水平",
        "positive": False,
        "high": "压力负担较高，需优先做任务拆解和减压安排。",
        "mid": "存在中等压力，建议每周固定安排恢复性活动。",
        "low": "压力可控，建议维持稳定学习节律。",
    },
    "social_isolation": {
        "label": "社交疏离",
        "positive": False,
        "high": "社交支持偏弱，建议主动连接同伴与可信任成人。",
        "mid": "社交状态一般，可通过小组合作提升归属感。",
        "low": "社交连接较稳定，可继续强化正向互动。",
    },
    "academic_pressure": {
        "label": "学业压力",
        "positive": False,
        "high": "学业压力较大，建议降低一次性目标，转为阶段目标。",
        "mid": "学业压力中等，适合用周计划降低焦虑。",
        "low": "学业压力可控，可保持稳步推进。",
    },
    "sleep_quality": {
        "label": "睡眠质量",
        "positive": True,
        "high": "睡眠质量较好，是当前心理恢复的重要保护因素。",
        "mid": "睡眠一般，建议固定入睡时间并减少夜间刺激。",
        "low": "睡眠不足已影响稳定性，建议把睡眠作为第一优先级。",
    },
    "attention_focus": {
        "label": "专注困难",
        "positive": False,
        "high": "专注困难较明显，建议使用番茄时段和环境减干扰策略。",
        "mid": "专注状态有波动，可通过短周期任务稳定注意力。",
        "low": "专注状态较好，可增加深度学习时段。",
    },
    "mood_low_energy": {
        "label": "低落无力",
        "positive": False,
        "high": "低落和疲惫感偏明显，建议优先恢复作息与运动。",
        "mid": "动力阶段性下降，建议从小任务启动恢复掌控感。",
        "low": "情绪能量总体良好，可保持节奏。",
    },
    "risk_behaviors": {
        "label": "风险行为倾向",
        "positive": False,
        "high": "冲动或冒险倾向偏高，需强化规则边界与复盘机制。",
        "mid": "偶发冲动行为，建议提前约定应对预案。",
        "low": "风险行为总体可控，继续保持明确边界。",
    },
    "self_harm_signal": {
        "label": "自伤信号",
        "positive": False,
        "high": "已出现较高风险信号，建议尽快转专业支持渠道。",
        "mid": "存在一定风险线索，建议持续观察并寻求专业评估。",
        "low": "未见明显自伤风险信号，仍需持续关注。",
    },
}


def _risk_label(tier: str) -> str:
    return {"low": "低风险", "medium": "中风险", "high": "高风险"}.get(tier, tier)


def _dimension_level(key: str, value: int) -> str:
    positive = bool(_DIMENSION_META.get(key, {}).get("positive", False))
    if positive:
        if value >= 4:
            return "good"
        if value >= 3:
            return "mid"
        return "bad"
    if value >= 4:
        return "bad"
    if value >= 3:
        return "mid"
    return "good"


def _dimension_message(key: str, level: str) -> str:
    meta = _DIMENSION_META.get(key, {})
    if level == "bad":
        return str(meta.get("high", "该维度需要重点关注。"))
    if level == "mid":
        return str(meta.get("mid", "该维度处于中等水平，可持续观察。"))
    return str(meta.get("low", "该维度整体稳定。"))


def _dimension_level_label(level: str) -> str:
    return {"good": "稳定/保护", "mid": "需关注", "bad": "重点关注"}.get(level, "需关注")


def _top_concerns(dimensions: dict[str, int]) -> list[str]:
    concern_pairs: list[tuple[str, float]] = []
    for key, value in dimensions.items():
        if key == "sleep_quality":
            severity = float(6 - int(value))
        else:
            severity = float(value)
        concern_pairs.append((key, severity))
    concern_pairs.sort(key=lambda x: x[1], reverse=True)
    out: list[str] = []
    for key, _score in concern_pairs[:3]:
        label = _DIMENSION_META.get(key, {}).get("label", key)
        out.append(str(label))
    return out


def _top_concern_dimension_keys(dimensions: dict[str, Any], limit: int = 3) -> list[str]:
    """Return dimension keys sorted by concern severity (same weighting as `_top_concerns`)."""
    concern_pairs: list[tuple[str, float]] = []
    for key, value in dimensions.items():
        if not isinstance(value, int):
            continue
        if key == "sleep_quality":
            severity = float(6 - int(value))
        else:
            severity = float(value)
        concern_pairs.append((key, severity))
    concern_pairs.sort(key=lambda x: x[1], reverse=True)
    return [k for k, _ in concern_pairs[:limit]]


_FLAG_ACTION_HINTS: dict[str, str] = {
    "self_harm_concern": "问卷出现自伤相关线索：建议由监护人陪同尽快联系专业机构或医院心理服务进行评估与支持。",
    "sdq_emotional_distress": "情绪相关条目偏突出：近期减少“道理压制”，多用倾听与情绪命名，并固定一个可期待的安抚仪式（散步、听固定音乐等）。",
    "sdq_attention_hyperactivity": "注意力与坐不住线索偏突出：学习环境做减法，任务用 10–15 分钟短段并写清“完成标准”。",
    "sdq_peer_relation_strain": "同伴关系条目偏突出：先稳住安全感与归属感，再讨论矛盾细节；必要时请班主任做中性协调。",
    "sdq_conduct_regulation_risk": "冲动与对抗线索偏突出：事先约定冷却信号与复盘时间，冲突当下先保边界与人身安全。",
    "sdq_low_prosocial_behavior": "亲社会互动偏低：安排小额“帮助他人/合作完成”的场景，并及时给具体肯定。",
    "elevated_stress": "压力感偏高：把目标拆小并明确“今天只要完成这一件”，同时保留每周恢复性活动。",
    "poor_sleep": "睡眠线索偏弱：优先固定起床时间，睡前减少屏幕与刺激性沟通。",
    "social_distress": "社交支持偏弱：用两人或三人小组活动建立安全互动，再逐步扩大社交挑战。",
    "low_mood_energy": "低落无力线索偏多：用可执行微小行动重启掌控感，并同步关注作息、运动与日照。",
}


def _prioritize_flags(flags: list[str]) -> list[str]:
    ranked: list[str] = []
    for f in _FLAG_ACTION_HINTS:
        if f in flags:
            ranked.append(f)
    for f in flags:
        if f not in ranked:
            ranked.append(f)
    return ranked


def build_recommended_actions(
    *,
    scores: dict[str, Any],
    profile: dict[str, Any],
    forecast_summary: dict[str, Any],
    questionnaire: dict[str, Any] | None,
) -> list[str]:
    """
    非危机场景下的「建议行动」：结合观察分、维度、标签、五行养育与流年摘要，
    避免仅按风险等级输出固定两句话。
    """
    out: list[str] = []
    seen: set[str] = set()

    def add(text: str) -> None:
        t = str(text).strip()
        if not t or t in seen:
            return
        seen.add(t)
        out.append(t)

    tier = str(scores.get("risk_tier") or "medium")
    wellbeing = scores.get("mental_wellbeing_score")
    try:
        wb = float(wellbeing)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        wb = 0.0

    add(
        f"心理健康观察分约 {wb:.1f} 分，当前分层为{_risk_label(tier)}。"
        "下列条目已结合问卷维度、提示标签、五行养育要点与流年节奏做了组合，可优先选 2–3 项落地。"
    )

    flags = [f for f in (scores.get("flags") or []) if isinstance(f, str)]
    n_flag = 0
    for flag in _prioritize_flags(flags):
        hint = _FLAG_ACTION_HINTS.get(flag)
        if hint:
            add(hint)
            n_flag += 1
        if n_flag >= 2:
            break

    dims_raw = scores.get("dimensions") or {}
    dims = {k: v for k, v in dims_raw.items() if isinstance(v, int)}
    for key in _top_concern_dimension_keys(dims, limit=2):
        level = _dimension_level(key, int(dims[key]))
        if level in ("bad", "mid"):
            add(_dimension_message(key, level))

    parenting = profile.get("parenting_guidance") or []
    if isinstance(parenting, list) and parenting:
        idx = (int(wb) + len(flags)) % len(parenting)
        add(str(parenting[idx]))

    peaks = forecast_summary.get("forecast_peak_years") or []
    troughs = forecast_summary.get("forecast_trough_years") or []
    if isinstance(peaks, list) and isinstance(troughs, list) and (peaks or troughs):
        pk = "、".join(str(int(y)) for y in peaks[:4])
        tr = "、".join(str(int(y)) for y in troughs[:4])
        add(
            f"流年预测（综合走势）相对更强的年份：{pk or '—'}；更宜减负稳态的年份：{tr or '—'}，"
            "可提前与家庭/孩子对齐节奏与期望。"
        )

    notes = str((questionnaire or {}).get("notes", "")).strip()
    if notes:
        snippet = notes if len(notes) <= 140 else notes[:137] + "…"
        add(f"结合补充说明，近期沟通可围绕：{snippet}")

    if tier == "high" and len(out) < 4:
        add("建议尽快联系学校心理老师或正规心理咨询机构做进一步评估（本工具不能替代专业评估）。")
        add("家庭优先：固定亲子对话时间、降低责备语气、保证睡眠与运动底线。")
    elif tier == "medium" and len(out) < 4:
        add("维持规律作息与户外活动；用「我们一起试试」替代「你应该」。")
        add("关注同伴关系与校园适应；必要时寻求班主任协同支持。")
    elif tier == "low" and len(out) < 4:
        add("保持每周至少一次「无评判」的亲子聊天；记录三个成长亮点以便巩固自信。")
        add("继续强化优势科目与兴趣出口，用成就感对冲阶段性压力。")

    return out[:10]


_TEACHER_FLAG_SCRIPT: dict[str, str] = {
    "sdq_emotional_distress": "若观察到情绪波动：反馈宜具体、温和，避免在同伴面前扩大化评价。",
    "sdq_attention_hyperactivity": "若注意力与坐不住线索明显：任务分段布置、板书步骤清晰、减少同时多重口头指令。",
    "sdq_peer_relation_strain": "若同伴关系敏感：小组活动可做稳定配对，冲突先单独倾听再公开协调。",
    "sdq_conduct_regulation_risk": "若冲动对抗增多：先明确课堂边界与可预期后果，再安排课后一对一复盘。",
    "sdq_low_prosocial_behavior": "若合作与助人表现偏弱：可给承担感适中的小组角色，并及时点名具体进步。",
    "elevated_stress": "若压力线索偏高：作业与提问可先降难度与频率，用「完成一小段」替代「一次到位」。",
    "poor_sleep": "若涉及作息：可与家长协商作业弹性，强调连续睡眠窗口比熬夜补作业更重要。",
    "social_distress": "若社交支持偏弱：课堂上减少随机点名施压，多给准备时间再回答。",
    "low_mood_energy": "若低落无力线索偏多：表扬聚焦过程努力，任务目标先小后大，避免公开比较。",
}


def build_communication_script(
    *,
    scores: dict[str, Any],
    profile: dict[str, Any],
    crisis: bool,
) -> dict[str, str]:
    """家校沟通话术：随分层、维度、标签与画像变化，避免长期固定两句。"""
    if crisis:
        return {
            "for_parents": (
                "请先放下对成绩与对错的追问，用短句确认陪伴与安全，例如「我在这里」「我们先保证你安全」。"
                "避免争辩与说教，尽快联系专业人员，并让孩子身边有信任的成年人陪同。"
            ),
            "for_teachers": (
                "请避免在班级公开场合追问细节或施压；安排可信成人一对一陪伴，并转介学校心理老师、做好交接记录。"
                "课堂任务暂缓高要求，以稳定与安全为最高优先。"
            ),
        }

    tier = str(scores.get("risk_tier") or "medium")
    wellbeing = scores.get("mental_wellbeing_score")
    try:
        wb = float(wellbeing)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        wb = 0.0

    dims = {k: v for k, v in (scores.get("dimensions") or {}).items() if isinstance(v, int)}
    top_labels = _top_concerns(dims)
    flags = [f for f in (scores.get("flags") or []) if isinstance(f, str)]

    elem_zh = str(profile.get("element_label_zh") or "").strip()
    tag = str(profile.get("psychology_tag") or "").strip()
    summary = str(profile.get("psychology_summary") or "").strip()
    if len(summary) > 72:
        summary = summary[:69] + "…"

    ef = profile.get("emotion_and_friendship") or {}
    emo_style = str(ef.get("style") or "").strip()

    # —— 家长话术 ——
    parent_bits: list[str] = []
    if tier == "high":
        parent_bits.append(
            f"当前心理健康观察分约 {wb:.1f} 分（{_risk_label(tier)}），建议先稳住关系与安全，"
            "少用指责式连环提问，把「发生了什么」放在「你为什么不」之前。"
        )
    elif tier == "medium":
        parent_bits.append(
            f"当前心理健康观察分约 {wb:.1f} 分（{_risk_label(tier)}），"
            "可用「我听到……」开头复述感受，再邀请孩子一起想一个当天能完成的小办法。"
        )
    else:
        parent_bits.append(
            f"当前心理健康观察分约 {wb:.1f} 分（{_risk_label(tier)}），"
            "适合在散步、吃饭等轻松场景做短对话，先肯定过程努力，再轻量谈改进。"
        )

    if top_labels:
        joined = "、".join(top_labels[:2])
        parent_bits.append(f"谈到近况时，可先围绕「{joined}」慢一点问，避免一次追很多议题。")

    if emo_style:
        parent_bits.append(
            f"孩子在同伴与情绪上偏「{emo_style}」，可把目标从「立刻改正」调整为「先接住情绪，再谈下一步」。"
        )

    if elem_zh or tag:
        tail = f"{elem_zh}{'：' if elem_zh and tag else ''}{tag}" if (elem_zh or tag) else ""
        if summary:
            parent_bits.append(f"画像参考（{tail}）——{summary}" if tail else summary)
        elif tail:
            parent_bits.append(f"画像参考：{tail}。")

    parent_bits.append("可选用「我们一起试试」替代「你应该」，把改进拆成当天就能完成的一小步。")

    if "sdq_emotional_distress" in flags or "low_mood_energy" in flags:
        parent_bits.append("若孩子沉默或顶撞，先命名情绪再暂停十分钟，往往比当场讲道理更有效。")
    elif "sdq_attention_hyperactivity" in flags or "poor_sleep" in flags:
        parent_bits.append("若作息与分心突出，先把「固定起床 + 可见任务清单」立住，再谈成绩目标。")

    for_parents = "".join(parent_bits)

    # —— 老师话术 ——
    teacher_bits: list[str] = []
    if tier == "high":
        teacher_bits.append(
            "建议以非公开方式了解近况，避免当堂追问或排名刺激；与心理老师协同并保持简要家校沟通记录。"
        )
    elif tier == "medium":
        teacher_bits.append(
            "课堂反馈可先降频、降难度，用可执行的小目标建立掌控感，再逐步提高要求。"
        )
    else:
        teacher_bits.append(
            "可在小组合作中给承担感适中的角色，反馈多用过程性语言，点名具体进步点。"
        )

    n_tf = 0
    for flag in _prioritize_flags(flags):
        line = _TEACHER_FLAG_SCRIPT.get(flag)
        if line:
            teacher_bits.append(line)
            n_tf += 1
        if n_tf >= 2:
            break

    if not n_tf and top_labels:
        teacher_bits.append(
            f"与家长沟通时可对齐优先关注：{'、'.join(top_labels[:2])}，约定一致的支持措辞与节奏。"
        )

    teacher_bits.append("评价与提问尽量避免公开比较，先给准备时间再点名，减少意外施压。")

    for_teachers = "".join(teacher_bits)

    return {"for_parents": for_parents, "for_teachers": for_teachers}


def _timeline_comment(year_item: dict[str, Any]) -> str:
    focus = int(year_item.get("learning_focus", 3))
    wellbeing = int(year_item.get("wellbeing_hint", 3))
    if focus <= 2 or wellbeing <= 2:
        return "建议减负稳节奏，先保作息和情绪稳定。"
    if focus >= 5 and wellbeing >= 4:
        return "适合强化优势科目或项目挑战，但仍需防止过载。"
    return "维持稳定推进，关注阶段性复盘与小步优化。"


def build_detailed_report(
    *,
    scores: dict[str, Any],
    profile: dict[str, Any],
    curve: list[dict[str, Any]],
    peaks_troughs: dict[str, list[int]],
    crisis: bool,
    crisis_reasons: list[str],
    element_resolution: str,
) -> dict[str, Any]:
    dims = scores.get("dimensions", {}) if isinstance(scores, dict) else {}
    tier = str(scores.get("risk_tier", "medium"))
    wellbeing = scores.get("mental_wellbeing_score")
    flags = scores.get("flags", [])

    dimension_analysis: list[dict[str, Any]] = []
    for key, value in dims.items():
        if not isinstance(value, int):
            continue
        level = _dimension_level(key, value)
        dimension_analysis.append(
            {
                "key": key,
                "label": _DIMENSION_META.get(key, {}).get("label", key),
                "value": value,
                "level": _dimension_level_label(level),
                "interpretation": _dimension_message(key, level),
            }
        )

    top_focus = _top_concerns({k: v for k, v in dims.items() if isinstance(v, int)})
    peak_years = peaks_troughs.get("peak_years", [])
    trough_years = peaks_troughs.get("trough_years", [])
    forecast_scores = [
        float((row.get("forecast_indices") or {}).get("overall_index", 3))
        for row in curve
    ]
    forecast_peak_years: list[int] = []
    forecast_trough_years: list[int] = []
    if forecast_scores:
        max_score = max(forecast_scores)
        min_score = min(forecast_scores)
        for idx, row in enumerate(curve):
            year = int(row.get("year", 0))
            score = forecast_scores[idx]
            if score == max_score:
                forecast_peak_years.append(year)
            if score == min_score:
                forecast_trough_years.append(year)
    resolution_text = {
        "explicit_override": "使用了显式指定的五行类型",
        "birth_bazi_with_hour": "根据出生小时换算时辰，按完整八字四柱计算五行倾向",
        "birth_day_stem": "根据出生日期计算日干后映射五行",
        "questionnaire_affinities": "根据兴趣倾向问卷推断",
        "questionnaire_default": "使用默认问卷推断",
    }.get(element_resolution, element_resolution)

    key_findings = [
        f"当前综合风险等级为{_risk_label(tier)}，心理健康观察分为 {wellbeing}。",
        f"需要优先关注的维度：{ '、'.join(top_focus) if top_focus else '暂无' }。",
        f"成长曲线高峰年份：{peak_years or '暂无'}；低谷年份：{trough_years or '暂无'}。",
        f"流年预测曲线高峰年份：{forecast_peak_years or '暂无'}；低谷年份：{forecast_trough_years or '暂无'}。",
    ]
    if crisis:
        key_findings.insert(0, "检测到潜在危机信号，需优先执行安全支持与专业转介。")

    timeline = []
    for row in curve:
        year = row.get("year")
        timeline.append(
            {
                "year": year,
                "psych_state": row.get("psych_state", ""),
                "learning_focus": row.get("learning_focus"),
                "wellbeing_hint": row.get("wellbeing_hint"),
                "forecast_indices": row.get("forecast_indices", {}),
                "focus_comment": _timeline_comment(row),
                "family_action": row.get("guidance", ""),
                "watchout": row.get("concern", ""),
            }
        )

    action_plan = {
        "next_2_weeks": [
            "固定睡眠窗口（建议保证稳定入睡时间），优先恢复基础节律。",
            "把学习目标拆成 15-30 分钟小任务，减少拖延与对抗。",
            "每周至少 1 次无评判沟通，先听感受再谈改进。",
        ],
        "month_1_to_3": [
            "建立家校协同反馈节奏（建议每 2-4 周复盘一次）。",
            "围绕优势科目建立正反馈，避免只盯短板。",
            "在高压力周期保留运动与同伴互动，防止长期内耗。",
        ],
        "escalation": [
            "若出现明显自伤/自杀相关表达或行为，请立即转专业支持渠道。",
            "若连续 2-4 周状态持续恶化，建议尽快进行专业评估。",
        ],
    }
    if crisis:
        action_plan["next_2_weeks"] = [
            "立即确保人身安全，避免单独处于高风险环境。",
            "第一时间联系监护人、学校心理老师或当地专业机构。",
            "暂停以成绩为中心的沟通，优先稳定安全与情绪。",
        ]

    return {
        "overview": "本报告用于教育场景下的成长观察与家校沟通，不构成医学诊断。",
        "risk_snapshot": {
            "risk_tier": tier,
            "risk_tier_label": _risk_label(tier),
            "mental_wellbeing_score": wellbeing,
            "flags": flags,
            "crisis_escalation": crisis,
            "crisis_reasons": crisis_reasons,
        },
        "key_findings": key_findings,
        "profile_interpretation": {
            "element_label": profile.get("element_label_zh", ""),
            "psychology_tag": profile.get("psychology_tag", ""),
            "psychology_summary": profile.get("psychology_summary", ""),
            "deep_psychology_labels": profile.get("deep_psychology_labels", []),
            "health_constitution_advice": profile.get("health_constitution_advice", []),
            "personality_tags": profile.get("personality_tags", []),
            "subject_strengths": profile.get("subject_strengths", []),
            "potential_development_directions": profile.get("potential_development_directions", []),
            "parenting_guidance": profile.get("parenting_guidance", []),
            "hands_on_and_self_discipline": profile.get("hands_on_and_self_discipline", {}),
            "emotion_and_friendship": profile.get("emotion_and_friendship", {}),
            "element_resolution": resolution_text,
        },
        "dimension_analysis": dimension_analysis,
        "growth_timeline": timeline,
        "action_plan": action_plan,
        "communication_script": build_communication_script(scores=scores, profile=profile, crisis=crisis),
    }
