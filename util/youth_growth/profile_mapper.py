"""五行（日主倾向）与心理画像映射 — 知识源自项目 reference 文档归纳。"""
from __future__ import annotations

from typing import Any

from lunar_python import Solar

# 内部统一英文 key；展示用中文在 profile 中给出
ELEMENT_KEYS = ("water", "metal", "earth", "wood", "fire")

ELEMENT_LABELS_ZH: dict[str, str] = {
    "water": "水系（壬/癸）",
    "metal": "金系（庚/辛）",
    "earth": "土系（戊/己）",
    "wood": "木系（甲/乙）",
    "fire": "火系（丙/丁）",
}

ELEMENT_PSYCHOLOGY: dict[str, dict[str, str]] = {
    "water": {
        "tag": "高内耗型智者 / 隐秘的胜负欲",
        "summary": "思维敏捷、内省深；压力下易思虑过度，需安全感与节奏管理。",
    },
    "metal": {
        "tag": "完美主义执行官 / 规则防御型人格",
        "summary": "重规则与秩序；受挫时易僵硬或自我苛责，需要具体肯定与弹性目标。",
    },
    "earth": {
        "tag": "稳健型防御者 / 延迟满足",
        "summary": "稳重包容；节奏偏慢，压力下可能闷在心里，需要被看见与情绪命名。",
    },
    "wood": {
        "tag": "高敏感共情者 / 发散型创作者",
        "summary": "同理与探索欲强；压力下易急躁或退缩，需要结构与安全感并重。",
    },
    "fire": {
        "tag": "表现欲与情绪驱动型学习者",
        "summary": "热情外向；易冲动或焦躁，需要精力出口与情绪命名练习。",
    },
}

ELEMENT_SUBJECTS: dict[str, list[str]] = {
    "water": ["数学与逻辑", "编程与推理", "自然科学"],
    "metal": ["物理化学", "外语与规则类", "棋类与建模"],
    "earth": ["历史与传统", "手工实践", "需要长期积累的科目"],
    "wood": ["语文阅读与写作", "艺术与观察", "生命科学与人文表达"],
    "fire": ["演讲与表演", "体育与团队活动", "领导力与展示类任务"],
}

ELEMENT_POTENTIAL_DEVELOPMENT_DIRECTIONS: dict[str, list[str]] = {
    "water": [
        "数理与编程进阶（算法思维、信息学、数据分析）",
        "研究型学习路径（课题探究、实验设计、深度阅读）",
        "策略决策方向（竞赛规划、项目统筹、问题建模）",
    ],
    "metal": [
        "工程与规范路径（工程制图、机器人、实验规程）",
        "规则密集型学科进阶（物理、化学、语言规范训练）",
        "精细执行岗位潜力（质控、法政逻辑、系统管理）",
    ],
    "earth": [
        "长期项目沉淀路径（历史研究、作品集累积、实践档案）",
        "应用实践方向（手工工艺、农科观察、生活科学）",
        "组织支持型角色（班级管理、协作协调、稳定执行）",
    ],
    "wood": [
        "创意表达路径（写作、设计、内容创作、跨学科叙事）",
        "人文与生命关怀方向（心理、教育、社会观察）",
        "探索创新型项目（研究性学习、创客活动、创新比赛）",
    ],
    "fire": [
        "舞台与表达路径（演讲辩论、主持、表演、传播）",
        "团队带动方向（社团组织、活动策划、项目推进）",
        "行动导向实践（体育竞技、实战训练、领导力任务）",
    ],
}

ELEMENT_PARENTING_GUIDANCE: dict[str, list[str]] = {
    "water": [
        "先建立安全感再谈成绩，批评前先复述孩子感受。",
        "用“任务拆解+可见进步”替代一次性高要求。",
        "避免高压追问，固定每周一次低评判沟通。",
    ],
    "metal": [
        "肯定其规则感与责任感，同时允许阶段性不完美。",
        "冲突时少用“你必须”，多用“我们如何一起达成目标”。",
        "帮助其区分“标准”与“苛责”，减少自我攻击。",
    ],
    "earth": [
        "通过稳定作息和固定流程增强掌控感。",
        "鼓励主动表达需求，避免长期“闷着扛”。",
        "在稳态中增加小挑战，防止长期停留舒适区。",
    ],
    "wood": [
        "先接纳情绪，再引导结构化行动（先做什么、后做什么）。",
        "鼓励表达与创作，同时明确边界与完成标准。",
        "在人际敏感期多做共情式倾听，减少比较式评价。",
    ],
    "fire": [
        "先接住热情，再建立规则（节奏、收尾、复盘）。",
        "高情绪时避免当场定性，先降温后讨论对错。",
        "保留正向舞台与运动出口，帮助能量可控释放。",
    ],
}

ELEMENT_DEEP_PSYCHOLOGY_LABELS: dict[str, list[str]] = {
    "water": ["高敏锐内省", "隐性竞争驱动", "安全感依赖决策质量"],
    "metal": ["秩序与边界导向", "高标准自我评判", "规则受挫后防御增强"],
    "earth": ["稳定依恋取向", "慢热但持续投入", "压力下倾向内化沉默"],
    "wood": ["高共情高联想", "价值感驱动行为", "受评价影响情绪波动"],
    "fire": ["情绪与表现联动", "即时反馈敏感", "社交舞台驱动成长"],
}

ELEMENT_CONSTITUTION_ADVICE: dict[str, list[str]] = {
    "water": ["重视睡眠深度与节律，避免长期夜间过度用脑。", "注意腰肾与泌尿系统保养，保持稳定饮水与保暖。", "高压阶段配合低强度有氧，减少持续内耗。"],
    "metal": ["关注呼吸道与皮肤干燥，季节转换时加强防护。", "避免长期紧绷导致的肩颈与咬肌负担。", "使用规律呼吸训练降低应激峰值。"],
    "earth": ["重点维护脾胃与消化节律，规律进餐。", "增加日常步行和核心力量，避免久坐积滞。", "压力高时先稳作息再提强度。"],
    "wood": ["关注肝胆与筋骨拉伸，减少情绪型熬夜。", "保留户外活动和自然暴露，帮助情绪代谢。", "眼部与颈肩放松应作为学习间歇固定动作。"],
    "fire": ["关注心肺负荷与兴奋后恢复，避免连续高刺激。", "减少晚间高强度屏幕与竞技刺激。", "通过运动后放松流程稳定神经兴奋度。"],
}

ELEMENT_PERSONALITY_TAGS: dict[str, list[str]] = {
    "water": ["洞察型", "策略型", "慢热高韧性"],
    "metal": ["原则型", "执行型", "目标清晰型"],
    "earth": ["稳态型", "支撑型", "长期主义"],
    "wood": ["探索型", "共情型", "创意驱动型"],
    "fire": ["表现型", "感染型", "行动先导型"],
}

ELEMENT_HANDS_ON_DISCIPLINE: dict[str, dict[str, Any]] = {
    "water": {
        "strengths": ["复杂问题拆解能力强", "独立深度任务表现好"],
        "risks": ["启动慢、前期犹豫", "压力期拖延与回避并存"],
        "advice": ["采用 15 分钟启动法", "任务先可视化再执行", "每日固定收尾复盘 5 分钟"],
    },
    "metal": {
        "strengths": ["流程执行和精度控制好", "规范任务完成度高"],
        "risks": ["过度追求完美导致效率下降", "遇挫后僵化"],
        "advice": ["设置 80 分可交付标准", "用阶段里程碑代替一次到位", "每周做一次弹性目标训练"],
    },
    "earth": {
        "strengths": ["稳定输出，抗波动能力好", "耐心积累型任务突出"],
        "risks": ["节奏偏慢，易错过窗口", "舒适区黏性强"],
        "advice": ["固定时间块推进", "每周增加一次挑战任务", "以小项目产出促进行动速度"],
    },
    "wood": {
        "strengths": ["动手创造力强", "跨学科连接能力好"],
        "risks": ["发散过多导致收束不足", "情绪影响执行稳定性"],
        "advice": ["先定完成标准再创作", "双清单管理（灵感/执行）", "同伴共创后必须单独收尾"],
    },
    "fire": {
        "strengths": ["行动启动快", "团队任务带动性强"],
        "risks": ["冲动开工、收尾薄弱", "外界刺激过多影响专注"],
        "advice": ["采用番茄钟约束节奏", "任务中段加入检查点", "建立睡前去兴奋流程"],
    },
}

ELEMENT_EMOTION_FRIENDSHIP: dict[str, dict[str, Any]] = {
    "water": {
        "style": "重质量不重量，倾向深度少量关系。",
        "risks": ["受误解后容易回避沟通", "遇冲突时内耗时间长"],
        "advice": ["先表达感受再表达立场", "建立 1-2 位稳定支持同伴", "用书面复盘替代情绪压抑"],
    },
    "metal": {
        "style": "重边界与规则，关系选择谨慎。",
        "risks": ["评价语言偏硬，易引发对立", "在比较中放大输赢感"],
        "advice": ["冲突场景先复述对方观点", "把“对错”改成“目标一致”", "训练非暴力表达句式"],
    },
    "earth": {
        "style": "关系稳定、包容，倾向长期同伴。",
        "risks": ["不擅主动求助，容易闷压", "被动维持关系而消耗自己"],
        "advice": ["设每周一次主动社交", "明确个人边界与拒绝句式", "情绪低潮期优先寻求支持"],
    },
    "wood": {
        "style": "共情强、连接快，重情感回响。",
        "risks": ["受关系反馈影响波动大", "过度投入导致失衡"],
        "advice": ["练习情绪分级表达", "设置关系投入上限", "冲突后 24 小时内复盘沟通"],
    },
    "fire": {
        "style": "外向主动、社交能量高。",
        "risks": ["易在兴奋期言语过冲", "同伴影响下风险决策上升"],
        "advice": ["社交前设底线规则", "高情绪时延迟决策", "强化正向团队活动出口"],
    },
}

ZHI_MAIN_ELEMENT: dict[str, str] = {
    "子": "water",
    "丑": "earth",
    "寅": "wood",
    "卯": "wood",
    "辰": "earth",
    "巳": "fire",
    "午": "fire",
    "未": "earth",
    "申": "metal",
    "酉": "metal",
    "戌": "earth",
    "亥": "water",
}

SHI_CHEN_ORDER = (
    ("子", "子时", "23:00-00:59"),
    ("丑", "丑时", "01:00-02:59"),
    ("寅", "寅时", "03:00-04:59"),
    ("卯", "卯时", "05:00-06:59"),
    ("辰", "辰时", "07:00-08:59"),
    ("巳", "巳时", "09:00-10:59"),
    ("午", "午时", "11:00-12:59"),
    ("未", "未时", "13:00-14:59"),
    ("申", "申时", "15:00-16:59"),
    ("酉", "酉时", "17:00-18:59"),
    ("戌", "戌时", "19:00-20:59"),
    ("亥", "亥时", "21:00-22:59"),
)

DAY_GAN_TO_ELEMENT: dict[str, str] = {
    "甲": "wood",
    "乙": "wood",
    "丙": "fire",
    "丁": "fire",
    "戊": "earth",
    "己": "earth",
    "庚": "metal",
    "辛": "metal",
    "壬": "water",
    "癸": "water",
}


def _normalize_hour(hour: Any) -> int | None:
    try:
        h = int(hour)
    except (TypeError, ValueError):
        return None
    if 0 <= h <= 23:
        return h
    return None


def _hour_to_shichen(hour: int) -> dict[str, str]:
    idx = ((hour + 1) // 2) % 12
    zhi, name, time_range = SHI_CHEN_ORDER[idx]
    return {
        "hour_24": str(hour),
        "zhi": zhi,
        "name": name,
        "time_range": time_range,
    }


def analyze_birth_bazi(birth: dict[str, Any] | None) -> dict[str, Any] | None:
    if not birth or not all(k in birth for k in ("year", "month", "day")):
        return None
    try:
        year = int(birth["year"])
        month = int(birth["month"])
        day = int(birth["day"])
    except (TypeError, ValueError):
        return None
    hour = _normalize_hour(birth.get("hour"))
    if hour is None:
        try:
            lunar = Solar.fromYmd(year, month, day).getLunar()
            day_gan = lunar.getDayGan()
            day_element = DAY_GAN_TO_ELEMENT.get(day_gan, "earth")
            return {
                "calendar": "solar",
                "hour_used": False,
                "day_master_gan": day_gan,
                "day_master_element": day_element,
            }
        except Exception:
            return None
    try:
        lunar = Solar.fromYmdHms(year, month, day, hour, 0, 0).getLunar()
        eight = lunar.getEightChar()
        pillars = {
            "year": eight.getYear(),
            "month": eight.getMonth(),
            "day": eight.getDay(),
            "time": eight.getTime(),
        }
        gan = {
            "year": eight.getYearGan(),
            "month": eight.getMonthGan(),
            "day": eight.getDayGan(),
            "time": eight.getTimeGan(),
        }
        zhi = {
            "year": eight.getYearZhi(),
            "month": eight.getMonthZhi(),
            "day": eight.getDayZhi(),
            "time": eight.getTimeZhi(),
        }
        scores = {k: 0.0 for k in ELEMENT_KEYS}
        for g in gan.values():
            scores[DAY_GAN_TO_ELEMENT.get(g, "earth")] += 2.0
        for z in zhi.values():
            scores[ZHI_MAIN_ELEMENT.get(z, "earth")] += 1.0
        day_element = DAY_GAN_TO_ELEMENT.get(gan["day"], "earth")
        max_score = max(scores.values()) if scores else 0.0
        candidates = [k for k, v in scores.items() if v == max_score]
        dominant = day_element if day_element in candidates else candidates[0]
        return {
            "calendar": "solar",
            "hour_used": True,
            "input_hour": hour,
            "shichen": _hour_to_shichen(hour),
            "pillars": pillars,
            "gan": gan,
            "zhi": zhi,
            "day_master_gan": gan["day"],
            "day_master_element": day_element,
            "five_element_scores": scores,
            "dominant_element_from_bazi": dominant,
        }
    except Exception:
        return None


def _affinity_scores(q: dict[str, Any]) -> dict[str, float]:
    return {
        "water": float(q.get("affinity_logic_math", 3)),
        "metal": float(q.get("affinity_rules_precision", 3)),
        "earth": float(q.get("affinity_stability_practice", 3)),
        "wood": float(q.get("affinity_nature_humanities", 3)),
        "fire": float(q.get("affinity_expression_performance", 3)),
    }


def infer_element_from_questionnaire(q: dict[str, Any]) -> str:
    """
    启发式：用问卷中的倾向字段推断日主五行倾向（演示用）。
    若提供 element_type / dominant_element 则优先使用。
    """
    if not q:
        return "earth"
    explicit = q.get("dominant_element") or q.get("element_type")
    if isinstance(explicit, str) and explicit.lower() in ELEMENT_KEYS:
        return explicit.lower()
    # 简易映射：根据兴趣滑动条（1-5）
    scores = _affinity_scores(q)
    return max(scores, key=scores.get)


def infer_element_from_birth(year: int, month: int, day: int, hour: int | None = None) -> str:
    """
    使用真实历法：按公历生日计算「日干」，并映射到五行（日主）。
    映射关系：甲乙木、丙丁火、戊己土、庚辛金、壬癸水。
    """
    if hour is not None:
        analysis = analyze_birth_bazi({"year": year, "month": month, "day": day, "hour": hour})
        if analysis and analysis.get("hour_used"):
            return str(analysis.get("dominant_element_from_bazi", "earth"))
    day_gan = Solar.fromYmd(year, month, day).getLunar().getDayGan()
    return DAY_GAN_TO_ELEMENT.get(day_gan, "earth")


def resolve_element(
    *,
    birth: dict[str, Any] | None,
    questionnaire: dict[str, Any] | None,
    element_override: str | None,
) -> tuple[str, str]:
    """
    返回 (element_key, resolution_note)。
    """
    q = questionnaire or {}
    if element_override and element_override.lower() in ELEMENT_KEYS:
        return element_override.lower(), "explicit_override"
    has_birth = bool(birth and all(k in birth for k in ("year", "month", "day")))
    if has_birth:
        try:
            hour = _normalize_hour(birth.get("hour"))
            el = infer_element_from_birth(
                int(birth["year"]),
                int(birth["month"]),
                int(birth["day"]),
                hour=hour,
            )
            if hour is not None:
                return el, "birth_bazi_with_hour"
            return el, "birth_day_stem"
        except Exception:
            # 生日无效或历法计算异常时，回退到问卷倾向。
            pass
    if any(k in q for k in ("affinity_logic_math", "dominant_element")):
        return infer_element_from_questionnaire(q), "questionnaire_affinities"
    return infer_element_from_questionnaire(q), "questionnaire_default"


def build_profile(element: str) -> dict[str, Any]:
    element = element if element in ELEMENT_KEYS else "earth"
    p = ELEMENT_PSYCHOLOGY[element]
    discipline = ELEMENT_HANDS_ON_DISCIPLINE[element]
    emotion_friendship = ELEMENT_EMOTION_FRIENDSHIP[element]
    return {
        "element_key": element,
        "element_label_zh": ELEMENT_LABELS_ZH[element],
        "psychology_tag": p["tag"],
        "psychology_summary": p["summary"],
        "deep_psychology_labels": ELEMENT_DEEP_PSYCHOLOGY_LABELS[element],
        "health_constitution_advice": ELEMENT_CONSTITUTION_ADVICE[element],
        "personality_tags": ELEMENT_PERSONALITY_TAGS[element],
        "subject_strengths": ELEMENT_SUBJECTS[element],
        "potential_development_directions": ELEMENT_POTENTIAL_DEVELOPMENT_DIRECTIONS[element],
        "parenting_guidance": ELEMENT_PARENTING_GUIDANCE[element],
        "hands_on_and_self_discipline": {
            "strengths": discipline["strengths"],
            "risks": discipline["risks"],
            "advice": discipline["advice"],
        },
        "emotion_and_friendship": {
            "style": emotion_friendship["style"],
            "risks": emotion_friendship["risks"],
            "advice": emotion_friendship["advice"],
        },
    }
