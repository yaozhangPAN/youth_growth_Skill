"""Tests for bazi_insights educational personalization."""
from __future__ import annotations

from util.youth_growth.bazi_insights import build_personalization_from_bazi, ten_god_name


def test_ten_god_jia_yi():
    assert ten_god_name("甲", "乙") == "劫财"
    assert ten_god_name("甲", "甲") == "比肩"


def test_personalization_from_full_bazi():
    bazi = {
        "hour_used": True,
        "day_master_gan": "甲",
        "day_master_element": "wood",
        "five_element_scores": {"wood": 8.0, "fire": 2.0, "earth": 1.0, "metal": 1.0, "water": 0.0},
        "gan": {"year": "庚", "month": "戊", "day": "甲", "time": "丙"},
        "zhi": {"year": "午", "month": "寅", "day": "子", "time": "寅"},
    }
    out = build_personalization_from_bazi(bazi)
    assert out.get("strength_label") == "偏旺"
    assert out.get("opening_line")
    assert any("水" in x or "复盘" in x for x in (out.get("parenting_hints") or []))


def test_branch_clash_hint():
    bazi = {
        "hour_used": True,
        "day_master_gan": "甲",
        "day_master_element": "wood",
        "five_element_scores": {"wood": 4.0, "fire": 4.0, "earth": 4.0, "metal": 4.0, "water": 4.0},
        "gan": {"year": "甲", "month": "甲", "day": "甲", "time": "甲"},
        "zhi": {"year": "子", "month": "午", "day": "寅", "time": "申"},
    }
    out = build_personalization_from_bazi(bazi)
    hints = (out.get("learning_hints") or []) + (out.get("parenting_hints") or [])
    assert any("急转弯" in h for h in hints)
