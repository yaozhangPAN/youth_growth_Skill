"""
基于出生结构（年月日时柱）的教育向个性化提示。
输出为「倾向 + 养育/学习建议」，不出现命理断语式措辞。
仅消费 analyze_birth_bazi 返回的结构化字段。
"""
from __future__ import annotations

from typing import Any

# 与 profile_mapper 一致，避免循环 import
_DAY_GAN_TO_ELEMENT: dict[str, str] = {
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
_ZHI_MAIN_ELEMENT: dict[str, str] = {
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
_ELEMENT_KEYS = ("water", "metal", "earth", "wood", "fire")
_YANG_STEMS = frozenset("甲丙戊庚壬")

# 地支六冲（用于「变化张力」类教育表述）
_CHONG_PAIRS: frozenset = frozenset(
    {
        ("子", "午"),
        ("午", "子"),
        ("卯", "酉"),
        ("酉", "卯"),
        ("寅", "申"),
        ("申", "寅"),
        ("巳", "亥"),
        ("亥", "巳"),
        ("辰", "戌"),
        ("戌", "辰"),
        ("丑", "未"),
        ("未", "丑"),
    }
)

# 月支 → 节律类提示（教育语境，不说「调候」字样）
_MONTH_ZHI_RHYTHM: dict[str, str] = {
    "寅": "开春前后精力起伏可能更明显，适合把目标拆小并以「周」为单位复盘。",
    "卯": "春季节奏里同伴与评价可能更敏感，可先稳住自尊再谈改进。",
    "辰": "换季期适合固定作息锚点，减少临时加任务带来的不确定感。",
    "巳": "气温升高阶段注意兴奋后的恢复流程，学习与运动之间留出冷却时间。",
    "午": "盛夏易燥动，安排可预测的休息与补水，减少「连轴转」式安排。",
    "未": "长夏湿热感偏重时，任务量宜分段，强调完成标准而非堆时长。",
    "申": "入秋后思维转细，适合清单化与错题复盘，避免只盯分数波动。",
    "酉": "秋燥期情绪可能更脆，批评宜短、具体、可执行。",
    "戌": "季节转换时规则感增强，说明「为什么」比强调服从更有效。",
    "亥": "入冬后向内收的能量上升，预留独处与低刺激恢复时段。",
    "子": "深冬宜保睡眠与保暖底线，减少夜间高刺激屏幕与争论。",
    "丑": "岁末压力大时，用「今天只完成一件」降低启动门槛。",
}


def _stem_element(g: str) -> str:
    return _DAY_GAN_TO_ELEMENT.get(g, "earth")


def _is_yang(g: str) -> bool:
    return g in _YANG_STEMS


def ten_god_name(day_gan: str, other_gan: str) -> str:
    """日主天干与其他天干的十神（用于内部分布，不直接对用户输出）。"""
    if day_gan == other_gan:
        return "比肩"
    de = _stem_element(day_gan)
    oe = _stem_element(other_gan)
    dy = _is_yang(day_gan)
    oy = _is_yang(other_gan)
    ei = _ELEMENT_KEYS.index(de)
    oi = _ELEMENT_KEYS.index(oe)
    if de == oe:
        return "比肩" if dy == oy else "劫财"
    if (ei + 1) % 5 == oi:
        return "食神" if dy == oy else "伤官"
    if (oi + 1) % 5 == ei:
        return "偏印" if dy == oy else "正印"
    if (ei + 2) % 5 == oi:
        return "偏财" if dy == oy else "正财"
    if (oi + 2) % 5 == ei:
        return "七杀" if dy == oy else "正官"
    return "比劫"


def _collect_branch_pairs(zhi: dict[str, Any] | None) -> list[tuple[str, str]]:
    if not zhi or not isinstance(zhi, dict):
        return []
    order = ("year", "month", "day", "time")
    vals = [str(zhi.get(k) or "") for k in order if zhi.get(k)]
    pairs: list[tuple[str, str]] = []
    for i, a in enumerate(vals):
        if not a:
            continue
        for b in vals[i + 1 :]:
            if b:
                pairs.append((a, b))
    return pairs


def _branch_tension_hints(zhi: dict[str, Any] | None) -> list[str]:
    hints: list[str] = []
    for a, b in _collect_branch_pairs(zhi):
        if (a, b) in _CHONG_PAIRS:
            hints.append(
                "成长节奏里可能出现「急转弯」式变化（环境或任务切换），"
                "建议重要安排提前说明、留缓冲日，减少临时通知带来的应激。"
            )
            break
    return hints[:1]


def _month_zhi_rhythm(zhi: dict[str, Any] | None) -> str | None:
    if not zhi or not isinstance(zhi, dict):
        return None
    mz = str(zhi.get("month") or "")
    return _MONTH_ZHI_RHYTHM.get(mz)


def _day_master_strength_hint(
    scores: dict[str, float], day_element: str, day_gan: str
) -> tuple[str, list[str]]:
    """返回 (标签, 教育向短句列表)。标签：偏旺 / 偏弱 / 相对中和"""
    total = sum(float(scores.get(k, 0)) for k in _ELEMENT_KEYS)
    if total <= 0:
        return "相对中和", []
    de = day_element if day_element in _ELEMENT_KEYS else "earth"
    ratio = float(scores.get(de, 0)) / total
    hints: list[str] = []
    if ratio >= 0.34:
        label = "偏旺"
        hints.append(
            "自我驱动与坚持度可能较强，但也更容易在受挫时「硬扛」；"
            "养育上可多给「可退出的选择」与情绪命名，学习上用里程碑替代一口气冲刺。"
        )
    elif ratio <= 0.17:
        label = "偏弱"
        hints.append(
            "启动与持续可能需要更多外部支架；养育上适合固定小仪式与短承诺，"
            "学习上优先「可见进度」与同伴/成人陪伴式起步。"
        )
    else:
        label = "相对中和"
        hints.append(
            "整体结构上松紧度较均衡，仍建议用周计划与复盘把优势固定下来，避免靠意志力硬撑。"
        )
    return label, hints


def _element_sparse_hints(scores: dict[str, float]) -> list[str]:
    """五行偏枯 → 活动/情境类建议，不说缺某行。"""
    out: list[str] = []
    for k in _ELEMENT_KEYS:
        if float(scores.get(k, 0)) <= 0.0:
            if k == "wood":
                out.append(
                    "材料显示孩子在「探索—表达—联想」侧的体验可能偏少："
                    "可增加阅读讨论、自然观察、项目式小课题，用低评判方式练表达。"
                )
            elif k == "fire":
                out.append(
                    "材料显示孩子在「展示—行动—热情释放」侧的体验可能偏少："
                    "可安排适量运动、舞台式小任务或团队角色，帮助能量有安全出口。"
                )
            elif k == "earth":
                out.append(
                    "材料显示孩子在「稳定节奏—实践落地」侧的体验可能偏少："
                    "可用固定流程、家务/手工小目标增强掌控感，减少飘忽的任务切换。"
                )
            elif k == "metal":
                out.append(
                    "材料显示孩子在「规则—边界—精细执行」侧的练习可能偏少："
                    "可用清单、计时与「完成标准」可视化，逐步建立可预期的反馈。"
                )
            elif k == "water":
                out.append(
                    "材料显示孩子在「复盘—冷静思考—独处恢复」侧的空间可能偏少："
                    "可保留每日短复盘与低刺激独处时段，减少连续高压追问。"
                )
    return out[:2]


def _ten_god_distribution_hints(day_gan: str, gan: dict[str, Any] | None) -> list[str]:
    if not gan or not isinstance(gan, dict) or not day_gan:
        return []
    counts: dict[str, int] = {}
    for pillar in ("year", "month", "time"):
        g = str(gan.get(pillar) or "")
        if not g or g == day_gan:
            continue
        name = ten_god_name(day_gan, g)
        counts[name] = counts.get(name, 0) + 1
    hints: list[str] = []
    if counts.get("食神", 0) + counts.get("伤官", 0) >= 2:
        hints.append(
            "结构上「尝试与表达」的动力较突出：适合项目制与展示型学习，"
            "同时约定收尾与复盘，避免只开花不结果。"
        )
    if counts.get("正印", 0) + counts.get("偏印", 0) >= 2:
        hints.append(
            "结构上「示范与模仿」敏感：家长与老师的以身作则影响大，"
            "可提供清晰范例与脚手架，少用抽象大道理。"
        )
    if counts.get("正官", 0) + counts.get("七杀", 0) >= 2:
        hints.append(
            "结构上对「规则与结果」更敏感：需要边界清晰且语气稳定，"
            "批评聚焦行为不贴标签，并留出改正的具体路径。"
        )
    if counts.get("正财", 0) + counts.get("偏财", 0) >= 2:
        hints.append(
            "结构上对「反馈与收获感」更敏感：用具体进步证据与小额目标达成来稳住动机，"
            "减少空洞比较。"
        )
    if counts.get("比肩", 0) + counts.get("劫财", 0) >= 2:
        hints.append(
            "结构上「自主与同伴」张力更明显：可明确个人目标与合作分工，"
            "在小组任务里给清晰角色，减少模糊竞争。"
        )
    return hints[:2]


def build_personalization_from_bazi(bazi: dict[str, Any] | None) -> dict[str, Any]:
    """
    将八字结构信息转写为教育向分层叙事。
    若 bazi 不完整则返回空 dict。
    """
    if not bazi or not isinstance(bazi, dict):
        return {}

    scores = bazi.get("five_element_scores")
    gan = bazi.get("gan")
    zhi = bazi.get("zhi")
    day_gan = str(bazi.get("day_master_gan") or (gan or {}).get("day") or "")
    day_el = str(bazi.get("day_master_element") or "")
    hour_used = bool(bazi.get("hour_used"))

    if not isinstance(scores, dict) or not day_gan:
        return {}

    strength_label, strength_hints = _day_master_strength_hint(scores, day_el, day_gan)
    sparse = _element_sparse_hints({k: float(scores.get(k, 0)) for k in _ELEMENT_KEYS})
    tg = _ten_god_distribution_hints(day_gan, gan if isinstance(gan, dict) else None)
    rhythm = _month_zhi_rhythm(zhi if isinstance(zhi, dict) else None)
    clash = _branch_tension_hints(zhi if isinstance(zhi, dict) else None)

    parenting: list[str] = []
    learning: list[str] = []
    meta: list[str] = []

    meta.append(
        "出生时刻按北京时间理解；无准确时辰时，以下仅基于年月日三柱作粗粒度参考。"
        if not hour_used
        else "出生时刻按北京时间理解；以下结合年月日时柱作结构参考（非命运判断）。"
    )

    parenting.extend(strength_hints)
    parenting.extend(sparse)
    parenting.extend(tg)
    if rhythm:
        learning.append(rhythm)
    learning.extend(clash)

    opening = (
        f"从成长观察角度，孩子在节奏上呈现「{strength_label}」倾向："
        "以下建议用于家校沟通与日常安排，不代表固定人格或未来结果。"
    )

    return {
        "reference_model": "birth_structure_educational_v1",
        "hour_assumption": "北京时间",
        "pillars_complete": hour_used,
        "strength_label": strength_label,
        "opening_line": opening,
        "parenting_hints": parenting[:6],
        "learning_hints": learning[:4],
        "meta_notes": meta,
    }
