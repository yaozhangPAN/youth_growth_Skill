"""Safety keyword scanning tests."""
from __future__ import annotations

from util.youth_growth.safety import crisis_from_questionnaire, scan_text


def test_scan_text_detects():
    assert scan_text("我不想活了") is True
    assert scan_text("今天天气不错") is False


def test_crisis_from_self_harm_signal():
    crisis, reasons = crisis_from_questionnaire({"self_harm_signal": 4})
    assert crisis is True
    assert "self_harm_signal_high" in reasons
