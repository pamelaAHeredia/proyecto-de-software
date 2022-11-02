from pathlib import Path
from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    redirect,
    url_for,
    send_file,
)

from src.services.member import MemberService
from src.services.settings import SettingsService
from src.services.suscription import SuscriptionService
from src.web.forms.member import (
    FilterByDocForm,
    MemberForm,
    FilterSearchForm,
)
from src.errors import database
from src.web.helpers.auth import login_required, verify_permission


# Se define Blueprint de Socio
member_blueprint = Blueprint("members", __name__, url_prefix="/socios")

service = MemberService()
setting = SettingsService()


@member_blueprint.get("/")
@login_required
@verify_permission("member_index")
def index():
    filter_form = FilterSearchForm()
    page = request.args.get("page", 1, type=int)
    filter = request.args.get("filter")
    search = request.args.get("search")
    member_paginator = service.list_paginated_members(
        page, setting.get_items_per_page(), "members.index", filter, search
    )
    return render_template(
        "members/index.html", filter_form=filter_form, paginator=member_paginator
    )


@member_blueprint.route("/create", methods=["GET", "POST"])
@login_required
@verify_permission("member_create")
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
@verify_permission("member_update")
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


@member_blueprint.post("/change_activity/<int:member_id>")
@login_required
@verify_permission("member_change_activity")
def change_activity(member_id):
    change = service.change_activity_member(member_id)
    if not change:
        flash("El socio es moroso no se puede activar", "warning")
    return redirect(url_for("members.index"))


@member_blueprint.route("/filter_by", methods=["POST", "GET"])
@verify_permission("member_index")
def filter_by():
    filter_form = FilterSearchForm()
    if filter_form.validate_on_submit:
        page = request.args.get("page", 1, type=int)
        filter = filter_form.filter.data
        search = filter_form.search.data
        members_paginator = service.list_paginated_members(
            page, setting.get_items_per_page(), "members.index", filter, search
        )
        return render_template(
            "members/index.html", paginator=members_paginator, filter_form=filter_form
        )


@member_blueprint.route("/filter_by_dni", methods=["POST", "GET"])
@verify_permission("member_index")
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


@member_blueprint.route("/member_info/<id>", methods=["GET"])
@verify_permission("member_show")
def member_info(id):
    member = service.get_by_membership_number(id)
    return render_template("members/member_info.html", member=member)


@member_blueprint.get("/export_list")
@verify_permission("member_index")
def export_list():
    filter_by_status = request.args.get("filter_by_status")
    filter_by_last_name = request.args.get("filter_by_last_name")
    export_select = request.args.get("export_select")
    members = service.members_for_export(filter_by_status, filter_by_last_name)
    if export_select == "pdf":
        report = service.export_list_to_pdf(members, setting.get_items_per_page())
        filename = Path(report._filename).name
        return render_template("members/view_report.html", filename=filename)
    else:
        report = service.export_list_to_csv(members)
        filename = report.name
        return send_file(
            filename,
            mimetype="text/csv",
            download_name="report.csv",
            as_attachment=True,
        )
