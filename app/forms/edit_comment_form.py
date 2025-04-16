from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class EditCommentForm(FlaskForm):
    content = StringField('Content', validators=[
        DataRequired(message="Content is required."),
        Length(max=500, message="Content must be under 500 characters.")
    ])
