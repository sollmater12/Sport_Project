from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, EmailField, DecimalField, \
    SelectField, IntegerField
from wtforms.validators import DataRequired


class CoachRegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    nickname = StringField('Ваше имя в сети', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    country = SelectField('Страна', choices=[
        ("Россия", "Россия"),
        ("Казахстан", "Казахстан"),
        ("Китай", "Китай"), ], validators=[DataRequired()])

    education = StringField('Образование', validators=[DataRequired()])
    achievements = StringField('Достижения', validators=[DataRequired()])
    specialization = StringField('Специализация', validators=[DataRequired()])
    experience = StringField('Опыт работы', validators=[DataRequired()])

    submit = SubmitField('Войти')


class CoachLoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
