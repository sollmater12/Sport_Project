from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, EmailField, DecimalField, \
    SelectField, IntegerField
from wtforms.validators import DataRequired


class AddId(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    submit = SubmitField('Войти')


