from decimal import Decimal
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import session
from src.errors import database
from src.web.helpers.auth import login_required, verify_permission

# Se define Blueprint de Usuario
suscription_blueprint = Blueprint("suscription", __name__, url_prefix="/inscripciones")

@suscription_blueprint.get("/")
@login_required
def index():
    """Render de la lista de disciplinas con paginación"""
    page = request.args.get("page", 1, type=int)
    discipline_paginator = service.list_paginated_disciplines(
        page, 2, "discipline.index"
    )
    return render_template(
        "disciplines/index.html",
        paginator=discipline_paginator
    )
