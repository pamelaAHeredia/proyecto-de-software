import os
import imghdr
import base64
from flask import Flask, current_app, render_template, request, redirect, url_for, abort, Blueprint
from werkzeug.utils import secure_filename

from src.models.database import db
from src.models.club.member import Picture
from src.services.member import MemberService
from src.web.forms.license.forms import PictureForm

_service_member = MemberService()
app = current_app
license_blueprint = Blueprint("license", __name__, url_prefix="/carnet")

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0) 
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@license_blueprint.get("/<id>")
def index(id):
    
    form=PictureForm()
    return render_template('license/index.html', form=form, id=id)
    

@license_blueprint.post("/crop/<id>")
def crop_picture(id):
    print(id)
    uploaded_file = request.files.get('picture')
    if uploaded_file:
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(uploaded_file.stream):
                abort(400)

        member_picture = base64.b64encode(uploaded_file.read())
        file_type=uploaded_file.content_type
        return render_template('license/crop.html', file_type=file_type, file=member_picture.decode('utf-8'))
    return redirect(url_for("license.index"))

@license_blueprint.post("/upload")
def upload_picture():

    #     #uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    #     member = _service_member.get_by_membership_number(1)
        
    #     member_picture = Picture()
    #     member_picture.name= 'img1'
    #     member_picture.image_type = uploaded_file.content_type
    #     member_picture.image = base64.b64encode(uploaded_file.read())
    #     member.picture = member_picture
    #     db.session.commit()

    cropped_photo=request.form.get('cropped_img')
    cropped_photo_type=request.form.get('cropped_img_type')
    if cropped_photo:
        binary_photo = cropped_photo.split(',')[1].encode('utf-8')        
    return render_template('license/upload.html', image_type=cropped_photo_type, image=binary_photo.decode("utf-8"))
