from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, URL

class PinForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(),
        Length(max=100, message="Title must be under 100 characters.")
    ])
    media_url = StringField('Media URL', validators=[
        DataRequired(),
        URL(message="Must be a valid URL."),
        Length(max=500)
    ])
    description = StringField('Description', validators=[
        DataRequired(),
        Length(max=500, message="Description must be under 500 characters.")
    ])
