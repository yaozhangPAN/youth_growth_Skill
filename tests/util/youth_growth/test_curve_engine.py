"""curve_engine tests."""
from __future__ import annotations

from util.youth_growth.curve_engine import get_yearly_curve, peaks_and_troughs


def test_curve_length_and_years():
    c = get_yearly_curve("wood")
    assert len(c) == 6
    assert c[0]["year"] == 2026


def test_peaks_troughs_non_empty():
    c = get_yearly_curve("metal")
    pt = peaks_and_troughs(c)
    assert "trough_years" in pt and "peak_years" in pt


def test_unknown_element_falls_back_to_earth():
    c = get_yearly_curve("unknown")
    assert c[0]["year"] == 2026
