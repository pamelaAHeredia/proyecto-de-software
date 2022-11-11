from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField

class PictureForm(FlaskForm):
    picture = FileField('File')
    submit = SubmitField('Submit')