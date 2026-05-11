"""Skill 注册表：启动时扫描 skills/internal 并加载带 SKILL.md 的包。"""
from __future__ import annotations

import importlib
import inspect
from pathlib import Path
from typing import Any

from skills.base_skill import BaseSkill

_REGISTRY: dict[str, BaseSkill] | None = None


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _load_skill_classes() -> dict[str, BaseSkill]:
    root = _project_root()
    internal = root / "skills" / "internal"
    loaded: dict[str, BaseSkill] = {}
    if not internal.is_dir():
        return loaded

    for pkg_dir in sorted(internal.iterdir()):
        if not pkg_dir.is_dir():
            continue
        if not (pkg_dir / "SKILL.md").exists():
            continue
        skill_py = pkg_dir / "skill.py"
        if not skill_py.exists():
            # 纯 Markdown skill：未实现动态 LLM 加载器时跳过（本仓库仅支持方式 B）
            continue
        pkg_name = pkg_dir.name
        mod_path = f"skills.internal.{pkg_name}.skill"
        try:
            mod = importlib.import_module(mod_path)
        except Exception as exc:  # pragma: no cover - 启动失败应可见
            raise RuntimeError(f"Failed to import skill module {mod_path}: {exc}") from exc

        for _attr_name, obj in inspect.getmembers(mod, inspect.isclass):
            if obj is BaseSkill or not issubclass(obj, BaseSkill):
                continue
            if inspect.isabstract(obj):
                continue
            instance = obj()
            key = getattr(instance, "name", None) or pkg_name
            if not key:
                continue
            loaded[str(key)] = instance
    return loaded


def get_registry() -> dict[str, BaseSkill]:
    """返回 name -> BaseSkill 实例映射（单例）。"""
    global _REGISTRY
    if _REGISTRY is None:
        _REGISTRY = _load_skill_classes()
    return _REGISTRY


def reload_registry() -> dict[str, BaseSkill]:
    """测试用：强制重新加载。"""
    global _REGISTRY
    _REGISTRY = _load_skill_classes()
    return _REGISTRY
