from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    login = StringField('Логин', render_kw={"placeholder": "Введите логин"})
    name = StringField('Имя', render_kw={"placeholder": "Введите имя"})
    password = PasswordField('Пароль', render_kw={"placeholder": "Введите пароль"})
    email = StringField('E-mail', render_kw={"placeholder": "Введите почту"})
    theme = SelectField('Выбор темы', choices=[(1, 'Светлая'), (2, 'Тёмная')], default=1)
    submit = SubmitField('Зарегистрироваться')