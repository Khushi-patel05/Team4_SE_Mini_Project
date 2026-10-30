"""Medical history and prescription management module."""

from flask import Blueprint

medical_records_bp = Blueprint(
    "medical_records",
    __name__,
    url_prefix="/medical-records",
    template_folder="../templates/medical_records",
)

from .models import initialize_medical_records_db  # noqa: E402
from . import routes  # noqa: E402,F401
