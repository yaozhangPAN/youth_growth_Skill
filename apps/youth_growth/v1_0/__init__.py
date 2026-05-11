from flask import Blueprint

blueprint = Blueprint("youth_growth_v1_0", __name__)

from apps.youth_growth.v1_0 import routes  # noqa: E402,F401
