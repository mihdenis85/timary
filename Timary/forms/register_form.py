from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')