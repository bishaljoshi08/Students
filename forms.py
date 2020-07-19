from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length

class EntryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),Length(min=4, max=20)])
    roll_no = IntegerField('Roll No.', validators=[DataRequired()])
    phone = IntegerField('Phone', validators=[DataRequired()])