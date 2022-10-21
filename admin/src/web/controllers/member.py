from flask import Blueprint, request, render_template, flash, redirect, url_for

from src.services.member import MemberService
from src.services.settings import SettingsService
from src.services.suscription import SuscriptionService 
from src.web.forms.member import (
    FilterByDocForm,
    MemberForm,
    FilterForm,
    SearchByLastName,
)
from src.errors import database
from src.web.helpers.auth import login_required, verify_permission


# Se define Blueprint de Socio
member_blueprint = Blueprint("members", __name__, url_prefix="/socios")

service = MemberService()
setting = SettingsService()
suscription = SuscriptionService()


@member_blueprint.get("/")
@login_required
def index():
    filter_form = FilterForm()
    search_form = SearchByLastName()
    page = request.args.get("page", 1, type=int)
    member_paginator = service.list_paginated_members(
        page, setting.get_items_per_page(), "members.index", "Todos"
    )
    return render_template(
        "members/index.html", filter_form=filter_form, search_form=search_form, paginator=member_paginator
    )


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
            member = service.create_member(
                first_name=first_name,
                last_name=last_name,
                document_type=document_type,
                document_number=document_number,
                gender=gender,
                address=address,
                email=email,
                phone_number=phone_number,
            )
            suscription.associate_member(member.membership_number)
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


@member_blueprint.route("/filter_by", methods=["POST"])
def filter_by():
    filter_form = FilterForm()
    search_form = SearchByLastName()
    if filter_form.validate_on_submit:
        page = request.args.get("page", 1, type=int)
        filter = filter_form.filter.data
        members_paginator = service.list_paginated_members(
            page,
            setting.get_items_per_page(),
            "members.index",
            filter,
        )
        return render_template(
            "members/index.html",
            paginator=members_paginator,
            filter_form=filter_form, search_form=search_form
        )


@member_blueprint.route("/filter_by_dni", methods=["POST", "GET"])
def filter_by_doc():
    filter_form = FilterByDocForm()
    if request.method == "POST":
        if filter_form.validate_on_submit():
            doc_type = filter_form.document_type.data
            doc_number = filter_form.document_number.data
            member = service.find_member(doc_type, doc_number)
            return render_template("members/member_info.html", member=member)
    else:
        return render_template("members/search.html", filter_form=filter_form)



@member_blueprint.route("/search_by_last_name", methods=["POST"])
def search_by_last_name():
    search_form = SearchByLastName()
    filter_form = FilterForm()
    if search_form.validate_on_submit():
        last_name = search_form.last_name.data
        page = request.args.get("page", 1, type=int)
        members_paginator = service.list_paginated_last_name(
            page,
            setting.get_items_per_page(),
            "members.index",
            str(last_name)
        )
        return render_template(
            "members/index.html",
            paginator=members_paginator,
            search_form=search_form,filter_form = filter_form
        )
