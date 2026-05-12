"""日主与选类一致性（需 lunar-python）。"""
from __future__ import annotations

import pytest

pytest.importorskip("lunar_python", reason="lunar-python required")

from util.youth_growth.profile_mapper import (
    analyze_birth_bazi,
    infer_element_from_birth,
    resolve_element,
)


def test_1981_0727_day_master_is_bing_fire():
    """公历 1981-07-27 日柱丙午，日干丙为火。"""
    b = {"year": 1981, "month": 7, "day": 27, "hour": 5}
    a = analyze_birth_bazi(b)
    assert a is not None
    assert a.get("day_master_gan") == "丙"
    assert a.get("day_master_element") == "fire"
    assert a.get("dominant_element_from_bazi") == "metal"
    el = infer_element_from_birth(1981, 7, 27, hour=5)
    assert el == "fire"


def test_resolve_uses_day_master_not_dominant():
    el, note = resolve_element(
        birth={"year": 1981, "month": 7, "day": 27, "hour": 5},
        questionnaire={},
        element_override=None,
    )
    assert el == "fire"
    assert note == "birth_bazi_with_hour"


def test_build_profile_includes_family_education_voice():
    from util.youth_growth.profile_mapper import build_profile

    p = build_profile("wood")
    fe = p.get("family_education_voice") or {}
    assert fe.get("traits")
    assert isinstance(fe.get("strengths"), list)
    assert isinstance(fe.get("growth_edges"), list)
    assert fe.get("home_learning_tip")
