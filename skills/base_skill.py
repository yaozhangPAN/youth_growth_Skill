"""Skill 基类：run() 为唯一入口。"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseSkill(ABC):
    """内置 skill 需继承此类并实现 run。"""

    name: str = ""
    description: str = ""
    version: str = "1.0.0"

    @abstractmethod
    def run(self, user_input: str, **kwargs: Any) -> str:
        """由 HTTP invoke 或脚本调用；返回字符串（通常为 JSON）。"""
