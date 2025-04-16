from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired

class AddImageForm(FlaskForm):
    group_id = IntegerField('group Id', validators=[DataRequired()])
    post_id = IntegerField('post Id', validators=[DataRequired()])