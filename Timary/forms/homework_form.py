from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FileField, SubmitField
from wtforms.validators import DataRequired


class HomeworkForm(FlaskForm):
    task = StringField('Задание', validators=[DataRequired()], render_kw={"placeholder": "Задание"})
    lesson = StringField('Урок', validators=[DataRequired()], render_kw={"placeholder": "Урок"})
    end = DateField('Дата', validators=[DataRequired()])
    ready = StringField('Готовность', validators=[DataRequired()], render_kw={"placeholder": "Готовность"})
    file = FileField('Загрузить файлы')
    submit = SubmitField('Добавить')