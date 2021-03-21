from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()], render_kw={"placeholder": "Введите логин"})
    password = PasswordField('Пароль', render_kw={"placeholder": "Введите пароль"})
    submit = SubmitField('Авторизоваться')