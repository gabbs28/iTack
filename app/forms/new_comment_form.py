from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length

class NewCommentForm(FlaskForm):
    pin_id = IntegerField('Pin ID', validators=[DataRequired()])
    content = StringField('Content', validators=[
        DataRequired(),
        Length(max=500)
    ])
    notified = BooleanField('Notified', validators=[InputRequired()])
    submit = SubmitField('Submit')
