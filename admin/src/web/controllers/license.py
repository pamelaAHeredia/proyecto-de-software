import os
import imghdr
import base64
from pathlib import Path
from flask import (
    Flask,
    flash,
    current_app,
    render_template,
    request,
    redirect,
    url_for,
    abort,
    Blueprint,
    send_file
)
from werkzeug.utils import secure_filename

from src.models.database import db

from src.services.member import MemberService
from src.services.movement import MovementService
from src.web.forms.license.forms import PictureForm
from src.web.helpers.auth import login_required, verify_permission

_service_member = MemberService()
_service_movement = MovementService()
app = current_app
license_blueprint = Blueprint("license", __name__, url_prefix="/carnet")


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return "." + (format if format != "jpeg" else "jpg")


@license_blueprint.get("/<id>")
def index(id):
    form = PictureForm()
    return render_template("license/index.html", form=form, id=id)


@license_blueprint.post("/crop/<id>")
def crop_picture(id):
    uploaded_file = request.files.get("picture")
    if uploaded_file:
        filename = secure_filename(uploaded_file.filename)
        if filename != "":
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config[
                "UPLOAD_EXTENSIONS"
            ] or file_ext != validate_image(uploaded_file.stream):
                abort(400)

        member_picture = base64.b64encode(uploaded_file.read())
        file_type = uploaded_file.content_type
        return render_template(
            "license/crop.html",
            file_type=file_type,
            file=member_picture.decode("utf-8"),
            member_id=id,
        )
    return redirect(url_for("license.index"))


@license_blueprint.post("/upload")
def upload_picture():
    member_id = request.form.get("member_id")
    member = _service_member.get_by_membership_number(member_id)
    cropped_photo = request.form.get("cropped_img")
    cropped_photo_type = request.form.get("cropped_img_type")
    if cropped_photo:
        binary_photo = cropped_photo.split(",")[1].encode("utf-8")
        result = _service_member.save_member_photo(
            member, cropped_photo_type, binary_photo
        )
        if result:
            flash("Imagen guardada con éxito!", "success")
        else:
            flash("Error al salvar la foto", "danger")

    return redirect(url_for("members.index"))


@license_blueprint.get("/plantillaCarnet/<id>")
@login_required
@verify_permission("member_show")
def view_carnet(id):
    member = _service_member.get_by_membership_number(id)
    if member.picture is None:
        flash(
            "No se pude visualizar el carnet si el socio no posee imagen asignada",
            "danger",
        )
        return redirect(url_for("members.index"))
    else:
        file = member.picture.image
        file_type = member.picture.image_type
        qr_img = member.picture.qr_image
        is_defaulter = _service_movement.is_defaulter(member)
        return render_template(
            "license/carnet.html",
            member=member,
            is_defaulter=is_defaulter,
            file_type=file_type,
            file=file.decode("utf-8"),
            qr=qr_img.decode("utf-8"),
        )


@license_blueprint.get("/exportPdf/<id>")
@verify_permission("member_show")
def export_pdf(id):
    license_pdf = _service_member.license_to_pdf(id)
    filename = license_pdf._filename
    return send_file(
            filename,
            mimetype="text/pdf",
            download_name="report.pdf",
            as_attachment=True,
        )
   
