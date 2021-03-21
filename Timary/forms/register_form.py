from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()], render_kw={"placeholder": "Введите логин"})
    name = StringField('Имя', validators=[DataRequired()], render_kw={"placeholder": "Введите имя"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"placeholder": "Введите пароль"})
    email = StringField('E-mail', validators=[DataRequired()], render_kw={"placeholder": "Введите почту"})
    theme = SelectField('Выбор темы', validators=[DataRequired()], choices=[('light', 'Светлая'), ('dark', 'Тёмная')])
    submit = SubmitField('Зарегистрироваться')