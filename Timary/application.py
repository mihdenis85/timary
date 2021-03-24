import os
from datetime import timedelta

from flask import Flask, render_template, redirect, url_for, make_response, jsonify, session, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename

from Timary.data import db_session
from Timary.data.models import User, Timetable, Homework
from Timary.forms import RegisterForm, LoginForm, ChangeForm, TimetableForm, HomeworkForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very_secret_key_jwkjldjwkdjlkwdkwjdldwhifwifhwiuhiuefhwiufhiuehf0f9wwefw'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db = db_session.create_session()
    return db.query(User).get(user_id)


@app.route('/')
def index():
    return redirect('/timetable/0')


@app.route('/timetable/<num_of_week>')
def index_start(num_of_week):
    if current_user.is_anonymous:
        return render_template('main.html', len_task=0)
    if num_of_week != '0' and num_of_week != '1' and num_of_week != '2' and num_of_week != '-1' and num_of_week != '-2':
        return redirect('/timetable/0')
    db = db_session.create_session()
    lessons = db.query(Timetable).filter(Timetable.id == current_user.id).all()
    lessons1 = []
    lessons2 = []
    lessons3 = []
    lessons4 = []
    lessons5 = []
    lessons6 = []
    for lesson in lessons:
        if lesson.day_of_week == '1' and lesson.num_of_week == num_of_week:
            lessons1.append(lesson)
        elif lesson.day_of_week == '2' and lesson.num_of_week == num_of_week:
            lessons2.append(lesson)
        elif lesson.day_of_week == '3' and lesson.num_of_week == num_of_week:
            lessons3.append(lesson)
        elif lesson.day_of_week == '4' and lesson.num_of_week == num_of_week:
            lessons4.append(lesson)
        elif lesson.day_of_week == '5' and lesson.num_of_week == num_of_week:
            lessons5.append(lesson)
        elif lesson.day_of_week == '6' and lesson.num_of_week == num_of_week:
            lessons6.append(lesson)
    next_num = str(int(num_of_week) + 1)
    previous_num = str(int(num_of_week) - 1)
    if num_of_week == '0':
        message_of_week = 'На этой неделе'
    elif num_of_week == '-1':
        message_of_week = 'На предыдушей неделе'
    elif num_of_week == '-2':
        message_of_week = 'На позапрошлой неделе'
    elif num_of_week == '1':
        message_of_week = 'На следующей неделе'
    elif num_of_week == '2':
        message_of_week = 'На неделе после следующей'
    if lessons:
        return render_template('main.html', lessons=lessons, len_lesson=len(lessons), lessons1=lessons1, lessons2=lessons2,
                               lessons3=lessons3, lessons4=lessons4, lessons5=lessons5, lessons6=lessons6,
                               len_lesson1=len(lessons1), len_lesson2=len(lessons2), len_lesson3=len(lessons3),
                               len_lesson4=len(lessons4), len_lesson5=len(lessons5), len_lesson6=len(lessons6),
                               num_of_week=num_of_week, next_num=next_num,
                               previous_num=previous_num, message_of_week=message_of_week)
    else:
        return render_template('main.html', lessons=lessons, len_task=0, num_of_week=num_of_week,
                               next_num=next_num, previous_num=previous_num, message_of_week=message_of_week)


@app.route('/homework/<num_of_week>')
def homework(num_of_week):
    if current_user.is_anonymous:
        return render_template('homework.html', len_task=0)
    if num_of_week != '0' and num_of_week != '1' and num_of_week != '2' and num_of_week != '-1' and num_of_week != '-2':
        return redirect('/homework/0')
    db = db_session.create_session()
    tasks = db.query(Homework).filter(Homework.id == current_user.id).all()
    tasks1 = []
    tasks2 = []
    tasks3 = []
    tasks4 = []
    tasks5 = []
    tasks6 = []
    for task in tasks:
        if task.day_of_week == '1' and task.num_of_week == num_of_week:
            tasks1.append(task)
        elif task.day_of_week == '2' and task.num_of_week == num_of_week:
            tasks2.append(task)
        elif task.day_of_week == '3' and task.num_of_week == num_of_week:
            tasks3.append(task)
        elif task.day_of_week == '4' and task.num_of_week == num_of_week:
            tasks4.append(task)
        elif task.day_of_week == '5' and task.num_of_week == num_of_week:
            tasks5.append(task)
        elif task.day_of_week == '6' and task.num_of_week == num_of_week:
            tasks6.append(task)
    next_num = str(int(num_of_week) + 1)
    previous_num = str(int(num_of_week) - 1)
    if num_of_week == '0':
        message_of_week = 'На этой неделе'
    elif num_of_week == '-1':
        message_of_week = 'На предыдушей неделе'
    elif num_of_week == '-2':
        message_of_week = 'На позапрошлой неделе'
    elif num_of_week == '1':
        message_of_week = 'На следующей неделе'
    elif num_of_week == '2':
        message_of_week = 'На неделе после следующей'
    if tasks:
        return render_template('homework.html', tasks=tasks, len_task=len(tasks), tasks1=tasks1, tasks2=tasks2,
                               tasks3=tasks3, tasks4=tasks4, tasks5=tasks5, tasks6=tasks6,
                               len_task1=len(tasks1), len_task2=len(tasks2), len_task3=len(tasks3),
                               len_task4=len(tasks4), len_task5=len(tasks5), len_task6=len(tasks6),
                               num_of_week=num_of_week, next_num=next_num,
                               previous_num=previous_num, message_of_week=message_of_week)
    else:
        return render_template('homework.html', tasks=tasks, len_task=0, num_of_week=num_of_week,
                               next_num=next_num, previous_num=previous_num, message_of_week=message_of_week)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegisterForm()
    login_form = LoginForm()
    print(form.password.data)
    if form.password.data and form.login.data and form.name.data and form.email.data:
        if form.validate_on_submit():
            if len(form.password.data) < 6:
                return render_template('register_and_login.html', title='Твоя профессия',
                                       form=form, form1=login_form,
                                       message="Проверьте пароль")
            if form.password.data.isdigit() or form.password.data.isalpha():
                return render_template('register_and_login.html', title='Твоя профессия',
                                       form=form, form1=login_form,
                                       message="Проверьте пароль")
            if not form.login.data or not form.name.data or not form.email.data or not form.theme.data:
                return render_template('register_and_login.html', form=form, form1=login_form, login_form=login_form,
                                       message='Проверьте правильность заполнения полей')
            db = db_session.create_session()
            if db.query(User).filter(User.email == form.email.data).first() or \
                    db.query(User).filter(User.login == form.login.data).first():
                return render_template('register_and_login.html', title='Твоя профессия',
                                       form=form, form1=login_form,
                                       message="Такой пользователь уже существует")
            user = User(
                login=form.login.data,
                name=form.name.data,
                email=form.email.data,
                theme=form.theme.data
            )
            user.set_password(form.password.data)
            db.add(user)
            db.commit()
            login_user(user, remember=True)
            return redirect('/user_info')

    if login_form.validate_on_submit():
        db = db_session.create_session()
        user = db.query(User).filter(User.login == login_form.login.data).first()
        if not user:
            return render_template('register_and_login.html', form=form, form1=login_form, message1="Проверьте правильность заполнения полей",
                                   title='Твоя профессия')
        if user.check_password(login_form.password.data):
            login_user(user, remember=True)
            return redirect('/user_info')
        else:
            return render_template('register_and_login.html', form=form, form1=login_form, message1="Проверьте пароль", title='Твоя профессия')
    return render_template('register_and_login.html', title='Твоя профессия', form=form, form1=login_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user_info')
@login_required
def user_info():
    return render_template('user_info.html')


@app.route('/change', methods=['GET', 'POST'])
@login_required
def change():
    all_data = {
        'login': current_user.login,
        'name': current_user.name
    }
    change_form = ChangeForm(data=all_data)
    if change_form.validate_on_submit():
        db = db_session.create_session()
        password = change_form.password.data
        user_now = db.query(User).filter(User.id == current_user.id).first()
        if user_now.check_password(password):
            user_now.login = change_form.login.data
            user_now.name = change_form.name.data
            db.commit()
            return redirect('/user_info')
        else:
            return render_template('change.html', form=change_form, message="Неправильный пароль",
                                   title='Твоя профессия')
    return render_template('change.html', form=change_form,
                                   title='Твоя профессия')


@app.route('/add_timetable', methods=['GET', 'POST'])
@login_required
def add_timetable():
    timetable_form = TimetableForm()
    if timetable_form.validate_on_submit():
        db = db_session.create_session()
        timetable = Timetable()
        timetable.lesson = timetable_form.lesson.data
        timetable.room = timetable_form.room.data
        timetable.day_of_week = timetable_form.day_of_week.data
        timetable.num_of_week = timetable_form.num_of_week.data
        current_user.timetable.append(timetable)
        db.merge(current_user)
        db.commit()
        return redirect('/')
    return render_template('add_timetable.html', form=timetable_form)


@app.route('/add_homework', methods=['GET', 'POST'])
@login_required
def add_homework():
    homework_form = HomeworkForm()
    if homework_form.validate_on_submit():
        db = db_session.create_session()
        homework = Homework()
        homework.task = homework_form.task.data
        homework.lesson = homework_form.lesson.data
        homework.day_of_week = homework_form.day_of_week.data
        homework.num_of_week = homework_form.num_of_week.data
        homework.ready = homework_form.ready.data
        homework.file = homework_form.file.data
        current_user.homework.append(homework)
        db.merge(current_user)
        db.commit()
        return redirect('/homework/0')
    return render_template('add_homework.html', form=homework_form)





'''
@app.errorhandler(404)
def not_found(error):
    if current_user.is_authenticated:
        info = (current_user.name + ' ' + current_user.surname)
    else:
        info = 'Anonymous'
    er_txt = '404 not found: Такого адреса не существует'
    return render_template('error.html', title='Твоя профессия',
                           text=er_txt, useracc=info)



@app.errorhandler(401)
def unauth(error):
    er_txt = '401 not authorized: Пожалуйста, авторизуйтесь на сайте!'
    return render_template('error.html', title='Твоя профессия', text=er_txt)


@app.errorhandler(500)
def error_serv(error):
    er_text = 'Кажется, на сервере возникла ошибка. Выйдите на главную страницу и попробуйте снова'
    return render_template('error.html', title='Твоя профессия', text=er_text)
'''

from os import path
db_session.global_init(path.join(path.dirname(__file__), './db/project.db'))


def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
