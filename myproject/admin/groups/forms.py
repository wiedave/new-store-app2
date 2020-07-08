from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired,DataRequired


class GroupForm(FlaskForm):
    groupname = StringField('Nama Group',validators=[InputRequired()])

class SearchForm(FlaskForm):
    search= StringField(validators=[DataRequired()])
