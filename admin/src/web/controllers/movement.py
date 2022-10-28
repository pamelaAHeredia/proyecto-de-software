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


@movement_blueprint.route("/member_balance/<id>", methods=["GET", "POST"])
@login_required
# @verify_permission()
def member_balance(id):
    movement_form = CreateMovementForm()
    member = member_service.get_by_membership_number(id)

    if request.method == "POST":
        if movement_form.validate_on_submit:
            amount = movement_form.amount.data
            detail = movement_form.detail.data
            date = movement_form.date.data
            print(amount, detail, date)
            service.credit(amount, detail, member, date)
            flash("Pago registrado con éxito.", "success")

    page = request.args.get("page", 1, type=int)
    balance = service.get_balance(member)
    moves_paginator = service.list_paginated_movements(
        page,
        settings.get_items_per_page(),
        "movements.member_balance.{member.membership_number}",
        member
    )
    return render_template(
        "movements/member_balance.html",
        member=member,
        balance=balance,
        moves_paginator=moves_paginator,
        movement_form=movement_form,
    )
