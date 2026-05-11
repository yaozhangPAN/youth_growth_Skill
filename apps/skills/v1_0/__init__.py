from flask import Blueprint

blueprint = Blueprint("skills_v1_0", __name__)

from apps.skills.v1_0 import routes  # noqa: E402,F401
