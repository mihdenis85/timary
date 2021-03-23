from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FileField, SubmitField, SelectField
from wtforms.validators import DataRequired


class HomeworkForm(FlaskForm):
    task = StringField('Задание', validators=[DataRequired()], render_kw={"placeholder": "Задание"})
    lesson = StringField('Урок', validators=[DataRequired()], render_kw={"placeholder": "Урок"})
    day_of_week = SelectField('Выбор дня недели', choices=[('1', 'Понедельник'), ('2', 'Вторник'), ('3', 'Среда'),
                                                           ('4', 'Четверг'), ('5', 'Пятница'), ('6', 'Суббота')], default='1')
    num_of_week = SelectField('Выбор номера недели', choices=[('-2', '2 неделями ранее'), ('-1', '1 неделей ранее'),
                                                              ('0', 'На этой неделе'), ('1', 'На следующей неделе'),
                                                              ('2', 'На неделе после следующей')], default='0')
    ready = StringField('Готовность', validators=[DataRequired()], render_kw={"placeholder": "Готовность"})
    file = FileField('Загрузить файлы')
    submit = SubmitField('Добавить')