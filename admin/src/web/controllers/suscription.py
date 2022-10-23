from decimal import Decimal
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import session

from src.services.discipline import DisciplineService
from src.services.suscription import SuscriptionService
from src.services.member import MemberService
from src.services.membership import MembershipService
from src.errors import database
from src.web.helpers.auth import login_required, verify_permission
from src.web.forms.suscription import SuscriptionForm


service_discipline = DisciplineService()
service_suscription = SuscriptionService()
service_member = MemberService()
service_membership = MembershipService()

# Se define Blueprint de Usuario
suscription_blueprint = Blueprint("suscription", __name__, url_prefix="/inscripciones")


@suscription_blueprint.get("/")
@login_required
def index():
    page = request.args.get("page", 1, type=int)
    discipline_id = request.args.get("discipline_id", type=int)
    suscriptions_paginator = service_suscription.list_paginated_suscriptions(
        discipline_id, page, 2, "discipline.index"
    )
    return render_template(
        "suscription/index.html",
        paginator=suscriptions_paginator,
        discipline_id=discipline_id,
    )


@suscription_blueprint.route("/find_member/<discipline_id>", methods=["POST", "GET"])
@login_required
# @verify_permission("discipline_create")
def find_member(discipline_id):
    form = SuscriptionForm()
    member = None
    enrolled = False
    if request.method == "GET":
        discipline_id = request.args.get("discipline_id", type=int)
    else:
        if form.validate_on_submit():
            email = form.email.data
            member = service_member.find_member_by_mail(email=email)
            if not member:
                flash("No existe un socio con ese email", "danger")
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
# @verify_permission("discipline_create")
def enroll(member_id, discipline_id):
    membership = service_discipline.membership(discipline_id)
    member = service_member.get_by_membership_number(member_id)

    if service_suscription.enroll(member, membership):
        flash("Socio suscripto correctamente", "success")

    return redirect(url_for("suscription.index", discipline_id=discipline_id))


@suscription_blueprint.post("/leave/<int:member_id>/<int:discipline_id>")
@login_required
# @verify_permission("discipline_create")
def leave(member_id, discipline_id):
    membership = service_discipline.membership(discipline_id)
    member = service_member.get_by_membership_number(member_id)

    if service_suscription.leave(member, membership):
        flash("Socio dado de baja de la suscripcion correctamente", "success")
        # form = SuscriptionForm()
        # form.email.data = member.email
        # return render_template(
        #     "suscription/find_member.html",
        #     form=form,
        #     member=member,
        #     discipline_id=discipline_id,
        # )

    return redirect(url_for("suscription.index", discipline_id=discipline_id))
