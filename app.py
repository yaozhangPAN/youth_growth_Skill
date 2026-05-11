"""Flask entrypoint for Vercel and other WSGI/ASGI hosts.

Vercel expects `app` in `app.py` (or `tool.vercel.entrypoint` in pyproject.toml).
The application factory lives in `run.py`; this module re-exports the instance.
"""
from __future__ import annotations

from run import app

__all__ = ["app"]
