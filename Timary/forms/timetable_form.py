from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired


class TimetableForm(FlaskForm):
    lesson = StringField('Урок', validators=[DataRequired()], render_kw={"placeholder": "Урок"})
    room = StringField('Кабинет', validators=[DataRequired()], render_kw={"placeholder": "Кабинет"})
    day = DateField('Дата', validators=[DataRequired()])
    begin = TimeField('Время начала', validators=[DataRequired()])
    end = TimeField('Время окончания', validators=[DataRequired()])
    submit = SubmitField('Добавить')