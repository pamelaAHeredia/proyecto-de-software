from flask import Blueprint, request, render_template, flash, redirect, url_for

from src.services.member import MemberService
from src.web.forms.member import MemberForm
from src.errors import database
from src.web.helpers.auth import login_required, verify_permission


# Se define Blueprint de Socio
member_blueprint = Blueprint("members", __name__, url_prefix="/socios")

service = MemberService()


@member_blueprint.get("/")
@login_required
def index():
    """Por metodo GET pide la lista total de socios al modelo y lo renderiza en la vista"""
    page = request.args.get("page", 1, type=int)
    member_paginator = service.list_paginated_members(page, 2, "members.index")
    return render_template("members/index.html", paginator=member_paginator)


@member_blueprint.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """Por metodo POST toma del request los datos y se los pasa al modelo para que agregue un Socio,
    si no lo puede agregar lo informa"""
    form = MemberForm()
    if form.validate_on_submit():

        first_name = form.first_name.data
        last_name = form.last_name.data
        document_type = form.document_type.data
        document_number = form.document_number.data
        gender = form.gender.data
        address = form.address.data
        email = form.email.data
        phone_number = form.phone_number.data

        try:
            service.create_member(
                first_name=first_name,
                last_name=last_name,
                document_type=document_type,
                document_number=document_number,
                gender=gender,
                address=address,
                email=email,
                phone_number=phone_number,
            )
            flash("Socio guardado con éxito!", "success")
            return redirect(url_for("members.index"))
        except database.ExistingData as e:
            flash(e, "danger")
    return render_template("members/create.html", form=form)


@member_blueprint.route("/update/<int:member_id>", methods=["GET", "POST"])
@login_required
def update(member_id):
    """Por metodo POST toma del request los datos y se los pasa al modelo para que agregue un Socio,
    si no lo puede agregar lo informa"""
    form = MemberForm()
    if request.method == "GET":
        member = service.get_by_membership_number(id=member_id)
        form.first_name.data = member.first_name
        form.last_name.data = member.last_name
        form.document_type.data = member.document_type
        form.document_number.data = member.document_number
        form.gender.data = member.gender
        form.address.data = member.address
        form.email.data = member.email
        form.phone_number.data = member.phone_number

    else:
        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            document_type = form.document_type.data
            document_number = form.document_number.data
            gender = form.gender.data
            address = form.address.data
            email = form.email.data
            phone_number = form.phone_number.data

        try:
            service.update_member(
                id=member_id,
                first_name=first_name,
                last_name=last_name,
                document_type=document_type,
                document_number=document_number,
                gender=gender,
                address=address,
                email=email,
                phone_number=phone_number,
            )
            flash("Socio actualizado con éxito!", "success")
            return redirect(url_for("members.index"))
        except database.ExistingData as e:
            flash(e, "danger")
    return render_template("members/update.html", form=form, member_id=member_id)


@member_blueprint.post("/deactivate/<int:member_id>")
@login_required
def deactivate(member_id):
    service.deactivate_member(member_id)
    return redirect(url_for("members.index"))

@member_blueprint.post("/exportpdf") 
def export_pdf():
    list = request.form.items.__get__
    print(list)
    return redirect(url_for("members.index"))   


