from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired


class GroupForm(FlaskForm):
    groupname = StringField('Nama Group',validators=[InputRequired()])
