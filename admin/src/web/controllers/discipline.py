import datetime
from decimal import Decimal
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import session

from src.errors import database
from src.web.forms.discipline import CreateDisciplineForm, UpdateDisciplineForm
from src.web.helpers.auth import login_required, verify_permission

from src.services.discipline import DisciplineService
from src.services.settings import SettingsService
from src.services.suscription import SuscriptionService


# Se define Blueprint de Usuario
discipline_blueprint = Blueprint("discipline", __name__, url_prefix="/disciplinas")

service_discipline = DisciplineService()
service_settings = SettingsService()
service_suscription = SuscriptionService()

@discipline_blueprint.get("/")
@login_required
@verify_permission("discipline_index")
def index():
    """Render de la lista de disciplinas con paginación"""
    page = request.args.get("page", 1, type=int)
    discipline_paginator = service_discipline.list_paginated_disciplines(
        page, service_settings.get_items_per_page(), "discipline.index"
    )
    return render_template("disciplines/index.html", paginator=discipline_paginator)

@discipline_blueprint.route("/create", methods=["GET", "POST"])
@login_required
@verify_permission("discipline_create")
def create():
    form = CreateDisciplineForm()

    if form.validate_on_submit():

        name = form.name.data
        category = form.category.data
        instructor = form.instructor.data
        days_and_schedules = form.days_and_schedules.data
        registration_quota = form.registration_quota.data
        pays_per_year = form.pays_per_year.data
        amount = form.amount.data
        is_active = form.is_active.data

        try:
            service_discipline.create_discipline(
                name=name,
                category=category,
                instructor=instructor,
                days_and_schedules=days_and_schedules,
                registration_quota=registration_quota,
                pays_per_year=pays_per_year,
                amount=amount,
                is_active=is_active,
            )
            flash("Disciplina creada con éxito", "success")
            return redirect(url_for("discipline.index"))
        except database.MinValueValueError as e:
            flash(str(e), "danger")
        except database.ExistingData as e:
            flash(f"La disciplina: {name} - {category} ya existe.", "danger")

    return render_template("disciplines/create.html", form=form)


@discipline_blueprint.route("/update/<int:discipline_id>", methods=["GET", "POST"])
@login_required
@verify_permission("discipline_update")
def update(discipline_id):
    form = UpdateDisciplineForm()

    if request.method == "GET":
        discipline = service_discipline.find_discipline(id=discipline_id)
        form.name.data = discipline.name
        form.category.data = discipline.category
        form.instructor.data = discipline.instructor
        form.days_and_schedules.data = discipline.days_and_schedules
        form.registration_quota.data = discipline.registration_quota
        form.pays_per_year.data = discipline.pays_per_year
        form.amount.data = discipline.amount
        form.is_active.data = discipline.is_active
        # discipline_id = discipline_id

    else:
        if form.validate_on_submit():
            name = form.name.data
            category = form.category.data
            instructor = form.instructor.data
            days_and_schedules = form.days_and_schedules.data
            registration_quota = form.registration_quota.data
            pays_per_year = form.pays_per_year.data
            amount = form.amount.data
            is_active = form.is_active.data

            try:
                service_discipline.update_discipline(
                    id=discipline_id,
                    name=name,
                    category=category,
                    instructor=instructor,
                    days_and_schedules=days_and_schedules,
                    registration_quota=registration_quota,
                    pays_per_year=pays_per_year,
                    amount=amount,
                    is_active=is_active,
                )
                flash("Disciplina actualizada con éxito", "success")
                return redirect(url_for("discipline.index"))
            except database.MinValueValueError as e:
                flash(str(e), "danger")
            except database.ExistingData as e:
                flash(f"La disciplina: {name} - {category} ya existe.", "danger")
            except database.UpdateError as e:
                flash(str(e), "danger")

    return render_template(
        "disciplines/update.html", form=form, discipline_id=discipline_id
    )


@discipline_blueprint.post("/delete/<int:discipline_id>")
@login_required
@verify_permission("discipline_destroy")
def delete(discipline_id):
    if service_discipline.delete_discipline(discipline_id):
        flash("Disciplina eliminada correctamente", "success")

    return redirect(url_for("discipline.index"))