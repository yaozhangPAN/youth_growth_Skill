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
    "sdq_emotional_distress": (
        "情绪线索偏明显时，课堂上可以先把「评价」放慢，把「描述」放慢。"
        "若需要与孩子单独说话，可用平稳的语气邀请他描述身体感受或当下想法，避免在同伴面前展开细节。"
    ),
    "sdq_attention_hyperactivity": (
        "注意力与冲动线索并存时，建议把指令拆成单步、可检验的小目标，并在板书上留下可见的线索。"
        "提问前预留几秒准备时间，有助于降低紧张带来的走神。"
    ),
    "sdq_peer_relation_strain": (
        "同伴关系较敏感时，小组编排上尽量避免让孩子长时间处于边缘位置；出现冲突时，先单独倾听再协调。"
        "让孩子感到「我被公平对待」，往往比当场厘清对错更优先。"
    ),
    "sdq_conduct_regulation_risk": (
        "冲动与对抗升高时，课堂上先稳住边界与语气，课后再用较短时间复盘行为与后果。"
        "公开纠正容易触发羞耻与防御，私下沟通更利于孩子把规则内化。"
    ),
    "sdq_low_prosocial_behavior": (
        "合作与助人动机偏弱时，可安排轻量、可完成的任务，并在完成后具体反馈「你帮助到了谁」。"
        "被需要与胜任感，常常是亲社会行为的起点。"
    ),
    "elevated_stress": (
        "压力感偏高时，作业与课堂提问可适当减量或分层，让孩子体验到「我能完成」再逐步提高要求。"
    ),
    "poor_sleep": (
        "若与家长沟通作息，可温和地共同确认睡眠窗口与作业负荷，强调可持续的节奏比短期冲刺更重要。"
    ),
    "social_distress": (
        "社交支持偏弱时，课堂上减少突然点名与公开比较；需要发言时，先用眼神确认再给准备时间。"
    ),
    "low_mood_energy": (
        "低落与无力线索偏多时，反馈宜落在具体努力与微小进步上，减少横向对比，帮助孩子保留自我效能感。"
    ),
}


# 家长侧：咨询师口吻——验证感受、正常化、再给一条可行路径（避免段子式口语）
_PARENT_DIM_THERAPIST_LINES: dict[str, str] = {
    "情绪调节困难": (
        "情绪起伏较大时，孩子往往先需要被看见，而不是被说服。"
        "您可以先用自己的话复述他的感受，再轻轻问：此刻最困扰他的是什么；等情绪降温后，再讨论解决办法。"
    ),
    "压力水平": (
        "压力偏高时，孩子容易把「我必须扛住」写在脸上，却不说出口。"
        "不妨与他一起梳理本周安排，明确哪些可以暂缓，让他知道您站在减轻负担这一边。"
    ),
    "社交疏离": (
        "若在学校感到疏离，孩子有时会以沉默或回避来保护自尊。"
        "聊天时可以从具体情境入手，例如与谁相处较自在、哪一刻感到被排斥，再慢慢靠近他的担心。"
    ),
    "学业压力": (
        "学业压力上升时，目标过大容易触发拖延与对抗。"
        "可以把任务拆到「今天能完成的一小段」，完成后给予具体肯定，再约定下一步，会更容易建立合作感。"
    ),
    "睡眠质量": (
        "睡眠受扰时，情绪与注意力往往会连锁波动。"
        "建议把「稳定入睡与起床」作为家庭优先事项，睡前减少评判性对话，用可预期的安抚仪式帮助神经系统放松。"
    ),
    "专注困难": (
        "专注困难常与任务模糊、焦虑叠加有关。"
        "可以与孩子约定短时段专注与短暂休息的节奏，并把完成标准说清，减少「我到底要做到怎样」的不确定感。"
    ),
    "低落无力": (
        "低落与无力感出现时，催促振作常常适得其反。"
        "更重要的是让他感到被接纳：先照顾基本节律与身体需要，再以小步子恢复行动感。"
    ),
    "风险行为倾向": (
        "冲动行为背后，往往有未被说出的委屈或压力。"
        "当下先降低对抗强度，事后在安静环境里复盘：发生了什么、他需要什么、下次可以怎样彼此提醒。"
    ),
    "自伤信号": (
        "若孩子谈到伤害自己，请以严肃、稳定的态度回应，表达关心并确认安全。"
        "建议尽快联系专业机构或医院心理服务，由可信赖的成年人陪同，本工具不能替代评估与干预。"
    ),
}


def _parent_opening_therapist(tier: str, wb: float) -> str:
    score_clause = f"从问卷整合的感受来看，约在 {wb:.0f} 分附近。"
    if tier == "high":
        return (
            f"{score_clause}"
            "我想先和您确认一点：此刻孩子内在承受的压力可能偏大，您感到担忧是非常自然的反应。"
            "在沟通上，我会建议先把关系与安全放在前面，放慢节奏，再逐步触及学习与人际议题。"
        )
    if tier == "medium":
        return (
            f"{score_clause}"
            "这更像是一个需要被持续留意、但不必被灾难化的信号：既有值得关注之处，也仍有调整空间。"
            "您可以带着好奇与他谈谈最近的变化，而不是带着「必须立刻纠正」的紧迫感。"
        )
    return (
        f"{score_clause}"
        "整体状态相对平稳。此时更适合在日常相处里做轻量的倾听与鼓励，为后续可能出现的波动预留心理空间。"
    )


def _parent_temperament_therapist(profile: dict[str, Any]) -> str | None:
    summary = str(profile.get("psychology_summary") or "").strip()
    if not summary:
        return None
    first = summary.split("；")[0].strip()
    if len(first) > 80:
        first = first[:77] + "…"
    return (
        f"结合材料，孩子在气质与应对方式上，较常呈现为：{first}。"
        "这本身并无好坏之分，而是帮助我们理解：怎样的语速、距离与期待，会让他更容易感到被尊重与被支持。"
    )


def _parent_peer_emotion_therapist(emo_style: str) -> str | None:
    if not emo_style:
        return None
    return (
        f"在同伴与情绪方面，材料提示孩子可能表现为：{emo_style}。"
        "您可以尝试用开放式问题邀请他描述体验，例如当时身体与情绪的感受，再慢慢连接到他的需要；尽量避免用一句话为他下定义。"
    )


def _parent_lines_for_top_labels(top_labels: list[str]) -> list[str]:
    out: list[str] = []
    for lab in top_labels[:2]:
        line = _PARENT_DIM_THERAPIST_LINES.get(lab.strip())
        if line:
            out.append(line)
    return out


def _parent_closing_therapist(tier: str, flags: list[str], wb: float) -> str:
    """收尾略有变化，减少同一句结尾的模版感。"""
    seed = (len(flags) + int(wb)) % 3
    if seed == 0:
        return (
            "若您愿意，沟通时可以把目标定为「先让孩子感到被理解」，再讨论具体改进。"
            "改变常常是渐进的；您保持稳定的在场，本身就是重要的治疗性因素。"
        )
    if seed == 1:
        return (
            "最后想轻轻提醒您：不必追求一次谈话解决所有问题。"
            "把对话拆成多次、每次只触及一小点，往往更能被孩子消化与吸收。"
        )
    return (
        "当您感到无力时，也请关注自己的休息与支持系统。"
        "情绪稳定的家长，更容易成为孩子可依靠的容器——这同样是值得被照顾的部分。"
    )


def _teacher_opening_therapist(tier: str) -> str:
    if tier == "high":
        return (
            "从材料看，孩子当前可能需要更细致的保护与支持。"
            "建议尽量避免在公开场合追问隐私或施压比较；如需了解近况，以单独、保密的沟通方式更为稳妥。"
        )
    if tier == "medium":
        return (
            "孩子近期可能处于压力与调节之间的摆动期。"
            "课堂上的反馈若能兼顾结构与弹性，会更有利于他维持参与感与自尊。"
        )
    return (
        "整体适应尚可时，持续的过程性鼓励与清晰边界，仍有助于巩固他的自我效能感。"
        "小组任务中适度的参与与可见的进步，会是有益的强化。"
    )


def _teacher_closing_therapist(flags: list[str]) -> str:
    seed = len(flags) % 2
    if seed == 0:
        return (
            "与家长的沟通，可在事实与感受之间取得平衡：既传递观察，也邀请家长补充家庭情境。"
            "一致而温和的态度，往往比单一「正确方法」更能帮助孩子跨情境整合经验。"
        )
    return (
        "若您观察到持续恶化或安全风险，请及时走学校既定流程并记录关键信息。"
        "早期、协同的回应，通常比事后补救更能保护孩子的身心安全。"
    )


def build_communication_script(
    *,
    scores: dict[str, Any],
    profile: dict[str, Any],
    crisis: bool,
) -> dict[str, str]:
    """给家长 / 老师的沟通参考：亲切、有边界的心理咨询师口吻，少套话、少段子感。"""
    if crisis:
        return {
            "for_parents": (
                "此刻最重要的是安全与陪伴。\n\n"
                "请您先稳定自己的情绪，用简短、明确的语言让孩子知道：您在他身边，此刻不以批评或追问为主。"
                "请尽快联系具备资质的专业机构或医院心理服务，由可信赖的成年人陪同，本内容不能替代危机评估与干预。"
            ),
            "for_teachers": (
                "危机情境下，请先依学校流程保护孩子隐私与安全，避免在班级内展开细节讨论。\n\n"
                "建议由指定教师单独陪伴并转介学校心理老师，做好简要记录；课业要求可暂时降级，以稳定为第一优先。"
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

    emo_style = str((profile.get("emotion_and_friendship") or {}).get("style") or "").strip()

    parent_parts: list[str] = [_parent_opening_therapist(tier, wb)]

    # 微调顺序：减少每次同一骨架的「模版感」
    dim_chunks = _parent_lines_for_top_labels(top_labels)
    temp_line = _parent_temperament_therapist(profile)
    peer_line = _parent_peer_emotion_therapist(emo_style)
    use_dim_first = (int(wb) + len(flags)) % 2 == 0
    if use_dim_first:
        parent_parts.extend(dim_chunks)
        if temp_line:
            parent_parts.append(temp_line)
        if peer_line:
            parent_parts.append(peer_line)
    else:
        if temp_line:
            parent_parts.append(temp_line)
        if peer_line:
            parent_parts.append(peer_line)
        parent_parts.extend(dim_chunks)

    parent_parts.append(_parent_closing_therapist(tier, flags, wb))

    if "sdq_emotional_distress" in flags or "low_mood_energy" in flags:
        parent_parts.append(
            "若孩子长时间沉默或回避眼神，不必急于「撬开」话题。"
            "陪伴本身有时已是干预：您在场、可预期、不过度侵入，会帮助他慢慢恢复表达的勇气。"
        )
    elif "sdq_attention_hyperactivity" in flags or "poor_sleep" in flags:
        parent_parts.append(
            "节律与注意力常常相互影响。"
            "可优先与孩子协商一个可执行的作息与学习节奏，再讨论成绩目标，会更容易形成合作而非对抗。"
        )

    for_parents = "\n\n".join(parent_parts)

    teacher_parts: list[str] = [_teacher_opening_therapist(tier)]

    n_tf = 0
    for flag in _prioritize_flags(flags):
        line = _TEACHER_FLAG_SCRIPT.get(flag)
        if line:
            teacher_parts.append(line)
            n_tf += 1
        if n_tf >= 2:
            break

    if not n_tf and top_labels:
        plain = "、".join(top_labels[:2])
        teacher_parts.append(
            f"材料中较突出的关注点是「{plain}」。"
            "与家长沟通时，可用观察性语言描述课堂现象，并邀请家长补充家庭情境，以便形成一致的、低羞耻的支持方式。"
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
