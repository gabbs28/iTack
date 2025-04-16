from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired

class NewBoardForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    private = BooleanField('Private', validators=[InputRequired()])
    submit = SubmitField('Submit')
