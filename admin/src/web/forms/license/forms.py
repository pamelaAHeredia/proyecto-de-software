from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField

from flask_wtf.file import FileField, FileRequired, FileAllowed

class PictureForm(FlaskForm):
    picture = FileField('File')
    submit = SubmitField('Submit')