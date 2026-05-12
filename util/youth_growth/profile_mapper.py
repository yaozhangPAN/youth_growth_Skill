"""五行（日主倾向）与心理画像映射 — 知识源自项目 reference 文档归纳。"""
from __future__ import annotations

from typing import Any

from lunar_python import Solar

# 内部统一英文 key；展示用中文在 profile 中给出
ELEMENT_KEYS = ("water", "metal", "earth", "wood", "fire")

ELEMENT_LABELS_ZH: dict[str, str] = {
    "water": "水系宝宝",
    "metal": "金系宝宝",
    "earth": "土系宝宝",
    "wood": "木系宝宝",
    "fire": "火系宝宝",
}

ELEMENT_PSYCHOLOGY: dict[str, dict[str, str]] = {
    "water": {
        "tag": "水娃气质丨共情与情绪表达",
        "summary": "情感细腻、同理心强，善倾听与连结；压力下易情绪波动或钻牛角尖，宜先懂心情再谈办法。",
    },
    "metal": {
        "tag": "条理型丨重标准与可靠执行",
        "summary": "讲规则、重细节，做事有章法；遇挫时易苛责自己或变僵硬，需要具体肯定与弹性目标。",
    },
    "earth": {
        "tag": "土娃气质丨慢热务实",
        "summary": "节奏稳、耐看过程、观察细腻；启动偏慢、表达偏少，需要耐心等待与小步示范。",
    },
    "wood": {
        "tag": "风娃气质丨创意与联想",
        "summary": "点子多、对感兴趣的话题停不下来，理解与创造感强；有时想法飘、收束犹豫，可用清单把灵感落到步骤上。",
    },
    "fire": {
        "tag": "火娃气质丨热情与行动力",
        "summary": "能量足、行动快、自信敢试；观察与收尾常薄弱，课前预习抓全貌、学习中段多检查，思维导图有助于加深思考维度。",
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
        "先建立安全感再谈成绩；批评前先复述孩子的感受，把「你怎么又」换成「我看到你好像…」。",
        "用“任务拆解+可见进步”替代一次性高要求。",
        "避免高压追问，固定每周一次低评判沟通。",
    ],
    "metal": [
        "肯定其规则感与责任感，同时明确「够好即可交付」的标准，允许阶段性不完美。",
        "冲突时少用“你必须”，多用“我们如何一起达成目标”。",
        "帮助其区分“标准”与“苛责”，减少自我攻击。",
    ],
    "earth": [
        "通过稳定作息和固定流程增强掌控感；慢热不是懒，多给示范少催逼。",
        "鼓励主动表达需求，避免长期“闷着扛”。",
        "在稳态中增加小挑战，防止长期停留舒适区。",
    ],
    "wood": [
        "先接纳情绪，再引导结构化行动（先做什么、后做什么）；把发散当作资源，用清单收束。",
        "鼓励表达与创作，同时明确边界与完成标准。",
        "在人际敏感期多做共情式倾听，减少比较式评价。",
    ],
    "fire": [
        "先接住热情，再建立规则（节奏、收尾、复盘）；把冲劲导向「做完再玩」。",
        "高情绪时避免当场定性，先降温后讨论对错。",
        "保留正向舞台与运动出口，帮助能量可控释放。",
    ],
}

ELEMENT_DEEP_PSYCHOLOGY_LABELS: dict[str, list[str]] = {
    "water": ["情感敏锐", "重关系与共鸣", "压力下需被理解再行动"],
    "metal": ["重秩序与标准", "自我要求高", "受挫时需具体肯定"],
    "earth": ["慢热持续型", "观察先于表达", "压力下易内化"],
    "wood": ["联想丰富", "兴趣驱动表达", "需结构帮助收束"],
    "fire": ["行动启动快", "爱表现与反馈", "需中段检查与收尾习惯"],
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
        "advice": [
            "先定完成标准再创作；日常用「步骤清单」防飘（类似风型娃的复习巩固）",
            "双清单管理（灵感/执行）",
            "同伴共创后必须单独收尾",
        ],
    },
    "fire": {
        "strengths": ["行动启动快", "团队任务带动性强"],
        "risks": ["冲动开工、收尾薄弱", "外界刺激过多影响专注"],
        "advice": [
            "课前短时预习抓结构；用思维导图展开审题维度，减少粗心漏项",
            "采用番茄钟约束节奏",
            "任务中段加入检查点",
            "建立睡前去兴奋流程",
        ],
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

# 家庭教育读物式叙事（特点 / 优势 / 成长面），与日主五行 key 对应；金系单独用「条理型」表述。
ELEMENT_FAMILY_EDUCATION_FRAME: dict[str, dict[str, Any]] = {
    "water": {
        "reader_voice": "叙述风格参考常见「水娃」教养读物：把情绪当作信号，而非故意作对。",
        "traits": "情感丰富、同理心强，能为他人提供情绪支持；对关系与氛围敏感。",
        "strengths": ["善于表达感受", "交友不难，愿主动关心人", "倾听与共情是天然优势"],
        "growth_edges": [
            "压力下易片面坚持己见",
            "情绪上来时显得固执或闷",
            "需要家长先稳住语气再谈事",
        ],
        "home_learning_tip": "考试季：情绪平复后再改错；约定「冷静后再复盘」，减少当场硬顶。",
    },
    "metal": {
        "reader_voice": "金系在读物里常接近「重标准、重执行」的孩子：肯定其可靠，同时松绑完美主义。",
        "traits": "做事讲规矩、重细节与可预期结果，喜欢把事情做对、做完整。",
        "strengths": ["条理清晰、执行力强", "自我要求高、可托付任务", "擅长按步骤推进"],
        "growth_edges": [
            "易把「高标准」变成自我苛责",
            "受挫时语气变硬、易对立",
            "需要具体肯定而非笼统表扬",
        ],
        "home_learning_tip": "用「80 分先交卷」练习弹性；错题本分模块，减少一次改完的压迫感。",
    },
    "earth": {
        "reader_voice": "叙述贴近「土娃」：慢热不是落后，善观察、善积累，宜小步示范。",
        "traits": "不急着抢镜，更愿把功夫做扎实；观察先于表达，行动偏稳。",
        "strengths": ["逻辑清楚、循序渐进", "耐心做实务与积累型任务", "环境稳定时表现扎实"],
        "growth_edges": [
            "新任务启动偏慢",
            "口头表达偏弱时易被误解为「不配合」",
            "陌生场合易害羞退缩",
        ],
        "home_learning_tip": "学习前用 5 分钟「今天只做这一小步」口头约定；展示类任务可先在家预演一遍。",
    },
    "wood": {
        "reader_voice": "气质接近读物中的「风娃」：想法多是天赋，用清单与步骤帮助落地。",
        "traits": "点子多、联想快，对感兴趣的话题愿意说很多；创意与理解力强。",
        "strengths": ["创造力与理解力突出", "沟通与表达意愿强", "能把知识串成有趣的故事"],
        "growth_edges": [
            "想法有时跳得太快、不够落地",
            "收束任务时会犹豫或拖延",
            "自以为懂了但基础未必扎实",
        ],
        "home_learning_tip": "用「步骤清单」固定复习节奏；写作与综合题限时前先列提纲，防考场想太多做不完。",
    },
    "fire": {
        "reader_voice": "气质接近读物中的「火娃」：热情与行动力是优势，补观察与深度即可更稳。",
        "traits": "精力充沛、行动力强，做事有冲劲；自信、敢试、恢复快。",
        "strengths": ["热情、自信、有主见", "启动快、带动同伴", "受挫后较易翻篇"],
        "growth_edges": [
            "观察细节偏弱，易粗心漏条件",
            "想得不够深就动手，收尾常薄弱",
            "急躁时读题、作文易偏题",
        ],
        "home_learning_tip": "课前短时预习抓「大框架」；用思维导图展开审题角度；中段设「检查点」再往下做。",
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
            eight = lunar.getEightChar()
            day_gan = lunar.getDayGan()
            day_element = DAY_GAN_TO_ELEMENT.get(day_gan, "earth")
            gan = {
                "year": eight.getYearGan(),
                "month": eight.getMonthGan(),
                "day": eight.getDayGan(),
                "time": None,
            }
            zhi = {
                "year": eight.getYearZhi(),
                "month": eight.getMonthZhi(),
                "day": eight.getDayZhi(),
                "time": None,
            }
            pillars = {
                "year": eight.getYear(),
                "month": eight.getMonth(),
                "day": eight.getDay(),
                "time": None,
            }
            scores = {k: 0.0 for k in ELEMENT_KEYS}
            for g in (gan.get("year"), gan.get("month"), gan.get("day")):
                if g:
                    scores[DAY_GAN_TO_ELEMENT.get(str(g), "earth")] += 2.0
            for z in (zhi.get("year"), zhi.get("month"), zhi.get("day")):
                if z:
                    scores[ZHI_MAIN_ELEMENT.get(str(z), "earth")] += 1.0
            max_score = max(scores.values()) if scores else 0.0
            candidates = [k for k, v in scores.items() if v == max_score]
            dominant_three = day_element if day_element in candidates else candidates[0]
            return {
                "calendar": "solar",
                "hour_used": False,
                "hour_assumption_note": "未提供时辰时，仅使用年月日三柱作结构参考；时辰按北京时间。",
                "day_master_gan": day_gan,
                "day_master_element": day_element,
                "pillars": pillars,
                "gan": gan,
                "zhi": zhi,
                "five_element_scores": scores,
                "dominant_element_three_pillar": dominant_three,
            }
        except Exception:
            try:
                lunar = Solar.fromYmd(year, month, day).getLunar()
                day_gan = lunar.getDayGan()
                day_element = DAY_GAN_TO_ELEMENT.get(day_gan, "earth")
                return {
                    "calendar": "solar",
                    "hour_used": False,
                    "hour_assumption_note": "未提供时辰时，仅使用日干信息；时辰按北京时间。",
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
        # 盘面五行分数最高项（用于个性化分析），不等于「日主」；日主始终以日干为准。
        dominant = day_element if day_element in candidates else candidates[0]
        return {
            "calendar": "solar",
            "hour_used": True,
            "hour_assumption_note": "时辰按北京时间换算。",
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
    使用真实历法：按公历取四柱（有 hour 则用北京时间整点入盘），以「日干」映射五行（日主），
    作为曲线与画像条目的 element_key。映射：甲乙木、丙丁火、戊己土、庚辛金、壬癸水。

    说明：`analyze_birth_bazi` 中的 `dominant_element_from_bazi` 为盘面加权参考，不用于此处选类。
    """
    birth: dict[str, Any] = {"year": year, "month": month, "day": day}
    if hour is not None:
        birth["hour"] = hour
    analysis = analyze_birth_bazi(birth)
    if analysis and analysis.get("day_master_element"):
        return str(analysis["day_master_element"])
    try:
        day_gan = Solar.fromYmd(year, month, day).getLunar().getDayGan()
        return DAY_GAN_TO_ELEMENT.get(day_gan, "earth")
    except Exception:
        return "earth"


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


def build_profile(element: str, *, birth_bazi: dict[str, Any] | None = None) -> dict[str, Any]:
    element = element if element in ELEMENT_KEYS else "earth"
    p = ELEMENT_PSYCHOLOGY[element]
    discipline = ELEMENT_HANDS_ON_DISCIPLINE[element]
    emotion_friendship = ELEMENT_EMOTION_FRIENDSHIP[element]
    base_parenting = list(ELEMENT_PARENTING_GUIDANCE[element])
    out: dict[str, Any] = {
        "element_key": element,
        "element_label_zh": ELEMENT_LABELS_ZH[element],
        "psychology_tag": p["tag"],
        "psychology_summary": p["summary"],
        "deep_psychology_labels": ELEMENT_DEEP_PSYCHOLOGY_LABELS[element],
        "health_constitution_advice": ELEMENT_CONSTITUTION_ADVICE[element],
        "personality_tags": ELEMENT_PERSONALITY_TAGS[element],
        "subject_strengths": ELEMENT_SUBJECTS[element],
        "potential_development_directions": ELEMENT_POTENTIAL_DEVELOPMENT_DIRECTIONS[element],
        "parenting_guidance": base_parenting,
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
    fe_src = ELEMENT_FAMILY_EDUCATION_FRAME.get(element) or ELEMENT_FAMILY_EDUCATION_FRAME["earth"]
    out["family_education_voice"] = {
        "reader_voice": fe_src["reader_voice"],
        "traits": fe_src["traits"],
        "strengths": list(fe_src["strengths"]),
        "growth_edges": list(fe_src["growth_edges"]),
        "home_learning_tip": fe_src["home_learning_tip"],
    }
    if birth_bazi and isinstance(birth_bazi, dict):
        from util.youth_growth.bazi_insights import build_personalization_from_bazi

        pers = build_personalization_from_bazi(birth_bazi)
        if pers:
            out["personalized_from_birth_structure"] = pers
            ph = list(pers.get("parenting_hints") or [])
            lh = list(pers.get("learning_hints") or [])
            if ph:
                out["parenting_guidance"] = ph[:4] + base_parenting[:4]
            if lh:
                out["learning_rhythm_hints"] = lh
            ol = str(pers.get("opening_line") or "").strip()
            if ol:
                out["psychology_summary"] = f"{p['summary']} {ol}"
    return out
