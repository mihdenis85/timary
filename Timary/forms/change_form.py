from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class ChangeForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    password = PasswordField('Пароль', render_kw={"placeholder": "Введите пароль"})
    submit = SubmitField('Изменить')