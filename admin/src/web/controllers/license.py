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

@license_blueprint.get("/")
def index():
    form=PictureForm()
    return render_template('license/index.html', form=form)

@license_blueprint.post("/crop_image")
def upload_files():
    img_raw=request.form.get('send_crop')
    # print(f"aca: {request.form.get('send_crop')}")
    if img_raw:
        print("entre")
        # crop_hidden = request.form.get('send_crop')
        # print(crop_hidden)
    
    uploaded_file = request.files['picture']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            abort(400)
    #     #uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    #     member = _service_member.get_by_membership_number(1)
        
    #     member_picture = Picture()
    #     member_picture.name= 'img1'
    #     member_picture.image_type = uploaded_file.content_type
    #     member_picture.image = base64.b64encode(uploaded_file.read())
    #     member.picture = member_picture
    #     db.session.commit()
    member_picture = base64.b64encode(uploaded_file.read())
    file_type=uploaded_file.content_type
    return render_template('license/img_show.html', file_type=file_type, file=member_picture.decode('utf-8'))
    # return redirect(url_for('license.index'))