from datetime import datetime
from flask import Blueprint, request, render_template, flash, redirect, url_for

from src.web.helpers.auth import login_required, verify_permission
from src.services.movement import MovementService
from src.services.member import MemberService
from src.services.settings import SettingsService
from src.web.forms.movement import CreateMovementForm

movement_blueprint = Blueprint("movements", __name__, url_prefix="/movements")


service = MovementService()
member_service = MemberService()
settings = SettingsService()


@movement_blueprint.route("/member_balance/<member_id>", methods=["GET", "POST"])
@login_required
# @verify_permission("movement_create")
def member_balance(member_id):
    movement_form = CreateMovementForm()
    member = member_service.get_by_membership_number(member_id)
    balance = service.get_balance(member, all=True)
    
    if request.method == "POST":
        if movement_form.validate_on_submit:
            amount = movement_form.amount.data
            detail = movement_form.detail.data
            date = movement_form.date.data
            service.credit(amount, detail, member, date, True)
            flash("Pago registrado con éxito.", "success")

    page = request.args.get("page", 1, type=int)

    paginator = service.list_paginated_movements(
        page,
        settings.get_items_per_page(),
        'movements.member_balance',
        member
    )
    

    return render_template(
        "movements/member_balance.html",
        member=member,
        balance=balance,
        paginator=paginator,
        movement_form=movement_form,
    )

