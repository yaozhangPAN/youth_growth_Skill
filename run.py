"""本地开发入口：Flask 内置服务器。"""
from __future__ import annotations

import os
import sys

# 保证项目根目录在 Python 路径中（无需 pip install -e）
_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from apps import create_app  # noqa: E402

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("HTTP_PORT", "5005"))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("ENV", "dev") == "dev")
