"""Flask 应用工厂：注册 blueprint 与健康检查。"""
from __future__ import annotations

from flask import Flask, jsonify, render_template


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.post("/health")
    def health():
        return jsonify({"status": "ok", "service": "wms-ai-skill"})

    # 延迟导入以避免循环
    from apps.skills.v1_0 import blueprint as skills_bp  # noqa: WPS433
    from apps.youth_growth.v1_0 import blueprint as youth_bp  # noqa: WPS433

    app.register_blueprint(skills_bp)
    app.register_blueprint(youth_bp)

    return app
