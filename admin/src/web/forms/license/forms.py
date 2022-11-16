from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField


class PictureForm(FlaskForm):
    picture = FileField('File', validators=[
        FileRequired(),
        FileAllowed(['png', 'pdf', 'jpg'], "wrong format!")
    ])
    submit = SubmitField('Submit')