"""Pytest fixtures."""
from __future__ import annotations

import os
import sys

import pytest

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)


@pytest.fixture
def client():
    from apps import create_app
    from util.skill_registry import reload_registry

    reload_registry()
    app = create_app()
    app.config.update({"TESTING": True})
    with app.test_client() as c:
        yield c
