from decimal import Decimal
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import session

from src.errors import database
from src.web.helpers.auth import login_required, verify_permission
from src.web.forms.suscription import SuscriptionForm

from src.services.discipline import DisciplineService
from src.services.suscription import SuscriptionService
from src.services.member import MemberService
from src.services.membership import MembershipService
from src.services.settings import SettingsService



service_discipline = DisciplineService()
service_suscription = SuscriptionService()
service_member = MemberService()
service_membership = MembershipService()
service_settings = SettingsService()

# Se define Blueprint de Usuario
suscription_blueprint = Blueprint("suscription", __name__, url_prefix="/inscripciones")


@suscription_blueprint.get("/")
@login_required
@verify_permission("suscription_index")
def index():
    page = request.args.get("page", 1, type=int)
    discipline_id = request.args.get("discipline_id", type=int)
    discipline = service_discipline.find_discipline(discipline_id)
    has_quota = discipline.has_quota
    suscriptions_paginator = service_suscription.list_paginated_suscriptions(
        discipline_id, page, service_settings.get_items_per_page(), "discipline.index"
    )
    return render_template(
        "suscription/index.html",
        paginator=suscriptions_paginator,
        discipline_id=discipline_id,
        has_quota=has_quota,
    )


@suscription_blueprint.route("/find_member", methods=["GET", "POST"])
@login_required
@verify_permission("suscription_create")
def find_member():
    form = SuscriptionForm()
    member = None
    enrolled = False
    discipline_id = request.args.get("discipline_id", type=int)

    if form.validate_on_submit():
        doc_type = form.document_type.data
        doc_number = form.document_number.data
        member = service_member.find_member(
            document_type=doc_type, document_number=doc_number
        )
        if not member:
            flash("No existe un socio con ese documento", "danger")
        else:
            enrolled = service_membership.member_is_enrolled(
                member.membership_number, discipline_id
            )

    return render_template(
        "suscription/find_member.html",
        form=form,
        member=member,
        discipline_id=discipline_id,
        enrolled=enrolled,
    )


@suscription_blueprint.post("/enroll/<int:member_id>/<int:discipline_id>")
@login_required
@verify_permission("suscription_create")
def enroll(member_id, discipline_id):
    membership = service_discipline.membership(discipline_id)
    member = service_member.get_by_membership_number(member_id)
    able_to_suscribe = service_suscription.enroll(member, membership)
    if not able_to_suscribe["can_suscribe"]:
        for k, v in able_to_suscribe["reason"].items():
            if not v:
                flash(f"Imposible inscribir al socio. Razon: {k}: {v}.", "danger")
        
        return redirect(url_for("suscription.index", discipline_id=discipline_id))

    flash("Socio suscripto correctamente", "success")
    return redirect(url_for("suscription.index", discipline_id=discipline_id))


@suscription_blueprint.post("/leave/<int:suscription_id>/<int:discipline_id>")
@login_required
@verify_permission("suscription_destroy")
def leave(suscription_id, discipline_id):

    if service_suscription.leave(suscription_id):
        flash("Socio dado de baja de la suscripcion correctamente", "success")

    return redirect(url_for("suscription.index", discipline_id=discipline_id))
