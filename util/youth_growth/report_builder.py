"""Detailed report builder for education-facing narratives."""
from __future__ import annotations

from typing import Any

from util.youth_growth.notes_analysis import analyze_supplementary_notes


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
    na_actions = analyze_supplementary_notes(notes, dimensions=dims).get("extra_recommended_actions") or []
    for line in na_actions:
        add(line)
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
    "sdq_emotional_distress": "情绪线索偏明显时，先放慢评价、多描述事实；单独沟通时用平稳语气，避免在同伴前展开细节。",
    "sdq_attention_hyperactivity": "注意力与冲动并存时，指令拆成单步小目标，提问前留几秒准备时间。",
    "sdq_peer_relation_strain": "同伴敏感时，减少边缘站位与公开比较；冲突先单独倾听再协调。",
    "sdq_conduct_regulation_risk": "冲动对抗升高时，课上稳住边界与语气，课后再短复盘；公开纠正易触发羞耻。",
    "sdq_low_prosocial_behavior": "合作动机偏弱时，给轻量可完成任务，并具体反馈「你帮助到了谁」。",
    "elevated_stress": "压力偏高时，作业与提问可减量或分层，先让孩子体验到「我能完成」。",
    "poor_sleep": "与家长沟通作息时，共同确认睡眠窗口与作业负荷，强调可持续节奏。",
    "social_distress": "社交支持偏弱时，减少突然点名与公开比较；发言前先用眼神确认。",
    "low_mood_energy": "低落无力线索偏多时，反馈落在具体努力与微小进步上，少横向对比。",
}


# 家长侧：咨询师口吻——验证感受、正常化、再给一条可行路径（避免段子式口语）
_PARENT_DIM_THERAPIST_LINES: dict[str, str] = {
    "情绪调节困难": "情绪起伏大时，先复述感受再问困扰点，降温后再谈办法。",
    "压力水平": "压力偏高时，一起梳理本周安排，明确可暂缓项，表达您站在减负这一边。",
    "社交疏离": "从具体情境聊起：与谁较自在、何时感到被排斥，慢慢靠近担心。",
    "学业压力": "把任务拆到「今天一小段」，完成后具体肯定，再约定下一步。",
    "睡眠质量": "优先稳定入睡起床，睡前少评判，用简短安抚仪式帮助放松。",
    "专注困难": "约定短时段专注+休息，并把完成标准说清楚，减少不确定感。",
    "低落无力": "少催促，先接纳与照顾节律，再用很小步子恢复行动感。",
    "风险行为倾向": "当下降对抗，安静环境再复盘：发生了什么、需要什么、如何互相提醒。",
    "自伤信号": "若谈到伤害自己，请稳定回应、确认安全并尽快联系专业机构（本工具不能替代评估）。",
}


def _parent_opening_therapist(tier: str, wb: float) -> str:
    score_clause = f"从问卷整合的感受来看，约在 {wb:.0f} 分附近。"
    if tier == "high":
        return (
            f"{score_clause}"
            "压力信号偏强，建议先稳住关系与安全、放慢节奏，再谈学业与人际。"
        )
    if tier == "medium":
        return f"{score_clause}有需要留意之处，也可用好奇、非指责的方式聊聊最近变化。"
    return f"{score_clause}整体相对平稳，日常轻量倾听与鼓励即可。"


def _parent_temperament_therapist(profile: dict[str, Any]) -> str | None:
    summary = str(profile.get("psychology_summary") or "").strip()
    if not summary:
        return None
    first = summary.split("；")[0].strip()
    if len(first) > 72:
        first = first[:69] + "…"
    return f"气质与应对上，材料概述为：{first}；可依此微调语速与期待。"


def _parent_peer_emotion_therapist(emo_style: str) -> str | None:
    if not emo_style:
        return None
    style = emo_style if len(emo_style) <= 48 else emo_style[:45] + "…"
    return f"同伴与情绪方面，材料提示：{style}。可用开放提问听体验，避免一句话下定义。"


def _parent_lines_for_top_labels(top_labels: list[str]) -> list[str]:
    out: list[str] = []
    for lab in top_labels[:1]:
        line = _PARENT_DIM_THERAPIST_LINES.get(lab.strip())
        if line:
            out.append(line)
    return out


_LEVEL_ORDER_SCRIPT: dict[str, int] = {"重点关注": 0, "需关注": 1, "稳定/保护": 2}


def _dimension_top_for_report(
    dimension_analysis: list[dict[str, Any]],
    emphasis_keys: list[str],
) -> list[dict[str, Any]]:
    """在等级优先的前提下，将补充说明命中的、且为需关注以上的维度提前。"""
    if not emphasis_keys:
        return sorted(
            dimension_analysis,
            key=lambda x: (_LEVEL_ORDER_SCRIPT.get(str(x.get("level", "")), 9), str(x.get("key", ""))),
        )[:3]
    pr = {k: i for i, k in enumerate(emphasis_keys)}
    return sorted(
        dimension_analysis,
        key=lambda x: (
            _LEVEL_ORDER_SCRIPT.get(str(x.get("level", "")), 9),
            pr.get(str(x.get("key", "")), 99),
            str(x.get("key", "")),
        ),
    )[:3]


def _parent_personal_from_report(ctx: dict[str, Any]) -> list[str]:
    """从报告摘要中抽取短句，便于口头复述。"""
    out: list[str] = []
    tp = ctx.get("top_focus_labels")
    labels = [str(x) for x in tp if x] if isinstance(tp, list) else []

    py = ctx.get("peak_years") or []
    tw = ctx.get("trough_years") or []
    fy = ctx.get("forecast_peak_years") or []
    tv = ctx.get("forecast_trough_years") or []

    head_bits: list[str] = []
    if labels:
        head_bits.append("优先关注：" + "、".join(labels))
    if (isinstance(py, list) and py) or (isinstance(tw, list) and tw):
        py_s = "、".join(str(y) for y in py) if py else "—"
        tw_s = "、".join(str(y) for y in tw) if tw else "—"
        head_bits.append(f"曲线高峰/低谷年：{py_s} / {tw_s}")
    if (isinstance(fy, list) and fy) or (isinstance(tv, list) and tv):
        fy_s = "、".join(str(y) for y in fy) if fy else "—"
        tv_s = "、".join(str(y) for y in tv) if tv else "—"
        head_bits.append(f"流年：有利约{fy_s}；宜减负约{tv_s}")
    if head_bits:
        out.append("；".join(head_bits) + "（仅作节奏参考）。")

    snippets = ctx.get("timeline_snippets")
    if isinstance(snippets, list) and snippets:
        s0 = snippets[0]
        if isinstance(s0, dict):
            y = s0.get("year")
            ps = str(s0.get("psych_state") or "").strip()
            ga = str(s0.get("family_action") or "").strip()
            if y is not None and ps:
                ps_short = ps if len(ps) <= 64 else ps[:61] + "…"
                ga_short = f" 家庭侧：{ga}" if ga and len(ga) <= 40 else (f" 家庭侧：{ga[:37]}…" if ga else "")
                out.append(f"{y}年前后：{ps_short}{ga_short}")

    adj = str(ctx.get("notes_adjustment") or "").strip()
    if adj:
        out.append(adj)

    act = str(ctx.get("action_next_2_weeks") or "").strip()
    subs = ctx.get("subject_strengths")
    clean = [str(s) for s in subs if s][:2] if isinstance(subs, list) else []
    tail_bits: list[str] = []
    if act:
        act_s = act if len(act) <= 72 else act[:69] + "…"
        tail_bits.append("两周首条：" + act_s)
    if clean:
        tail_bits.append("优势切入：" + "、".join(clean))
    if tail_bits:
        out.append(" ".join(tail_bits))

    return out


def _parent_dimension_from_report(details: list[dict[str, Any]], *, limit: int = 1) -> list[str]:
    out: list[str] = []
    for item in details[:limit]:
        lab = str(item.get("label") or "").strip()
        interp = str(item.get("interpretation") or "").strip()
        lvl = str(item.get("level") or "").strip()
        if not lab or not interp:
            continue
        lvl_bit = f"（{lvl}）" if lvl else ""
        interp_s = interp if len(interp) <= 72 else interp[:69] + "…"
        out.append(f"「{lab}」{lvl_bit}报告要点：{interp_s}")
    return out


def _teacher_personal_from_report(ctx: dict[str, Any]) -> list[str]:
    out: list[str] = []
    details = ctx.get("dimension_details")
    if isinstance(details, list):
        for item in details[:1]:
            if not isinstance(item, dict):
                continue
            lab = str(item.get("label") or "").strip()
            interp = str(item.get("interpretation") or "").strip()
            if lab and interp:
                interp_s = interp if len(interp) <= 70 else interp[:67] + "…"
                out.append(f"与家长可点名「{lab}」：{interp_s}")
            break
    snippets = ctx.get("timeline_snippets")
    wo = ""
    if isinstance(snippets, list):
        for s in snippets[:1]:
            if not isinstance(s, dict):
                continue
            w = str(s.get("watchout") or "").strip()
            if w:
                wo = w if len(w) <= 48 else w[:45] + "…"
                break
    fy = ctx.get("forecast_peak_years") or []
    tv = ctx.get("forecast_trough_years") or []
    fy_s = "、".join(str(y) for y in fy) if isinstance(fy, list) and fy else ""
    tv_s = "、".join(str(y) for y in tv) if isinstance(tv, list) and tv else ""
    rhythm = ""
    if fy_s or tv_s:
        rhythm = f"流年约利{fy_s or '—'}、宜缓{tv_s or '—'}。"
    if wo and rhythm:
        out.append(f"留意信号：{wo} {rhythm}")
    elif wo:
        out.append(f"留意信号：{wo}")
    elif rhythm:
        out.append(rhythm)

    ern = str(ctx.get("element_resolution_note") or "").strip()
    if ern:
        ern_s = ern if len(ern) <= 44 else ern[:41] + "…"
        out.append(f"五行依据一句话即可：{ern_s}")
    return out


def _parent_closing_therapist(tier: str, flags: list[str], wb: float) -> str:
    """收尾略有变化，减少同一句结尾的模版感。"""
    seed = (len(flags) + int(wb)) % 3
    if seed == 0:
        return "沟通目标可先定为「被理解」再谈改进；渐进改变，您的稳定在场很重要。"
    if seed == 1:
        return "不必一次谈完：拆成多次、每次一小点，更容易被孩子吸收。"
    return "您也请关注自身休息；情绪稳定的家长，更容易成为孩子的支持容器。"


def _teacher_opening_therapist(tier: str) -> str:
    if tier == "high":
        return "材料提示需更强保护：避免公开追问隐私或施压比较，单独保密沟通更稳妥。"
    if tier == "medium":
        return "可能在压力与调节间摆动：课堂反馈兼顾结构与弹性，利于参与感与自尊。"
    return "适应尚可时，过程性鼓励与清晰边界仍有帮助；小组中适度参与与可见进步可作强化。"


def _teacher_closing_therapist(flags: list[str]) -> str:
    seed = len(flags) % 2
    if seed == 0:
        return "与家长沟通：事实与感受并重，邀请补充家庭情境；一致温和比单一「正确方法」更有效。"
    return "若见持续恶化或安全风险，请走校内流程并记录要点；早协同通常优于事后补救。"


def build_communication_script(
    *,
    scores: dict[str, Any],
    profile: dict[str, Any],
    crisis: bool,
    report_context: dict[str, Any] | None = None,
) -> dict[str, str]:
    """给家长 / 老师的沟通参考：亲切、有边界的心理咨询师口吻，少套话、少段子感。"""
    if crisis:
        parent_base = (
            "请以安全为先：稳定陪伴，少批评少追问；尽快联系专业机构或医院心理服务评估与干预（本内容不能替代专业处置）。"
        )
        teacher_base = (
            "请按学校危机流程：保护隐私、单独沟通、转介心理老师并做简要记录；课业先降级，以稳定为先。"
        )
        reasons: list[str] = []
        if report_context:
            raw = report_context.get("crisis_reasons")
            if isinstance(raw, list):
                reasons = [str(r) for r in raw if r]
        if reasons:
            joined = "；".join(reasons[:5])
            parent_base += "\n\n筛查线索：" + joined + "（转述专业人员即可）。"
            teacher_base += "\n\n客观记录：" + joined + "。"
        return {"for_parents": parent_base, "for_teachers": teacher_base}

    tier = str(scores.get("risk_tier") or "medium")
    wellbeing = scores.get("mental_wellbeing_score")
    try:
        wb = float(wellbeing)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        wb = 0.0

    dims = {k: v for k, v in (scores.get("dimensions") or {}).items() if isinstance(v, int)}
    top_labels = _top_concerns(dims)
    flags = [f for f in (scores.get("flags") or []) if isinstance(f, str)]

    emo_style = str((profile.get("emotion_and_friendship") or {}).get("style") or "").strip()

    parent_parts: list[str] = [_parent_opening_therapist(tier, wb)]
    has_report = bool(report_context)

    if has_report:
        parent_parts.extend(_parent_personal_from_report(report_context))  # type: ignore[arg-type]

    dim_chunks: list[str] = []
    if has_report:
        details = report_context.get("dimension_details")  # type: ignore[union-attr]
        if isinstance(details, list):
            dim_chunks = _parent_dimension_from_report([d for d in details if isinstance(d, dict)])
        if not dim_chunks:
            dim_chunks = _parent_lines_for_top_labels(top_labels)
    else:
        dim_chunks = _parent_lines_for_top_labels(top_labels)

    # 微调顺序：减少每次同一骨架的「模版感」
    temp_line = _parent_temperament_therapist(profile)
    peer_line = _parent_peer_emotion_therapist(emo_style)
    peer_use = None if has_report else peer_line
    use_dim_first = (int(wb) + len(flags)) % 2 == 0
    if use_dim_first:
        parent_parts.extend(dim_chunks)
        if temp_line:
            parent_parts.append(temp_line)
        if peer_use:
            parent_parts.append(peer_use)
    else:
        if temp_line:
            parent_parts.append(temp_line)
        if peer_use:
            parent_parts.append(peer_use)
        parent_parts.extend(dim_chunks)

    parent_parts.append(_parent_closing_therapist(tier, flags, wb))

    if "sdq_emotional_distress" in flags or "low_mood_energy" in flags:
        parent_parts.append("孩子沉默或回避时不必硬聊；在场与节律本身即支持。")
    elif "sdq_attention_hyperactivity" in flags or "poor_sleep" in flags:
        parent_parts.append("节律与注意力相互影响：先协商可执行的作息与学习节奏，再谈成绩目标。")

    for_parents = "\n\n".join(parent_parts)

    teacher_parts: list[str] = [_teacher_opening_therapist(tier)]
    if report_context:
        teacher_parts.extend(_teacher_personal_from_report(report_context))

    max_flag_lines = 1 if report_context else 2
    n_tf = 0
    for flag in _prioritize_flags(flags):
        line = _TEACHER_FLAG_SCRIPT.get(flag)
        if line:
            teacher_parts.append(line)
            n_tf += 1
        if n_tf >= max_flag_lines:
            break

    if not n_tf and top_labels:
        plain = "、".join(top_labels[:2])
        teacher_parts.append(
            f"材料关注点：{plain}。用观察性语言描述课堂现象，并请家长补充家庭情境。"
        )

    teacher_parts.append(_teacher_closing_therapist(flags))

    for_teachers = "\n\n".join(teacher_parts)

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
    questionnaire: dict[str, Any] | None = None,
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

    notes_raw = ""
    if questionnaire and isinstance(questionnaire, dict):
        notes_raw = str(questionnaire.get("notes") or "").strip()
    dims_int = {k: int(v) for k, v in dims.items() if isinstance(v, int)}
    na = analyze_supplementary_notes(notes_raw, dimensions=dims_int)
    adj_summary = str(na.get("adjustment_summary") or "").strip()
    if adj_summary:
        key_findings.insert(1, adj_summary)

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
    elif na.get("action_injections"):
        inject = list(na["action_injections"])[:2]
        action_plan["next_2_weeks"] = inject + action_plan["next_2_weeks"]

    dimension_top = _dimension_top_for_report(
        dimension_analysis,
        list(na.get("emphasis_dimension_keys") or []),
    )

    timeline_snippets: list[dict[str, Any]] = []
    for row in curve[:2]:
        if not isinstance(row, dict):
            continue
        timeline_snippets.append(
            {
                "year": row.get("year"),
                "psych_state": str(row.get("psych_state") or ""),
                "family_action": str(row.get("guidance") or ""),
                "watchout": str(row.get("concern") or ""),
            }
        )

    next_two = action_plan.get("next_2_weeks") or []
    action_first = str(next_two[0]) if next_two else ""
    subs_raw = profile.get("subject_strengths")
    strength_slice = subs_raw[:3] if isinstance(subs_raw, list) else []

    report_context: dict[str, Any] = {
        "top_focus_labels": top_focus,
        "peak_years": list(peak_years) if isinstance(peak_years, list) else [],
        "trough_years": list(trough_years) if isinstance(trough_years, list) else [],
        "forecast_peak_years": forecast_peak_years,
        "forecast_trough_years": forecast_trough_years,
        "dimension_details": dimension_top,
        "timeline_snippets": timeline_snippets,
        "action_next_2_weeks": action_first,
        "subject_strengths": strength_slice,
        "element_resolution_note": resolution_text,
        "crisis_reasons": list(crisis_reasons) if crisis_reasons else [],
        "notes_adjustment": adj_summary,
    }

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
        "supplementary_notes_analysis": {
            "has_notes": bool(na.get("has_notes")),
            "snippet": na.get("snippet", ""),
            "detected_themes": na.get("detected_themes", []),
            "theme_ids": na.get("theme_ids", []),
            "adjustment_summary": adj_summary,
        },
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
            "supplementary_notes_insights": {
                "themes": na.get("detected_themes", []),
                "theme_ids": na.get("theme_ids", []),
                "snippet": na.get("snippet", ""),
            },
        },
        "dimension_analysis": dimension_analysis,
        "growth_timeline": timeline,
        "action_plan": action_plan,
        "communication_script": build_communication_script(
            scores=scores, profile=profile, crisis=crisis, report_context=report_context
        ),
    }
