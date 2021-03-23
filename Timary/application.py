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
    return render_template('main.html', title='Timary Project')


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


@app.route('/homework')
@login_required
def homework():
    db = db_session.create_session()
    tasks = db.query(Homework).filter(Homework.id == current_user.id).all()
    print(len(tasks))
    if tasks:
        return render_template('homework.html', tasks=tasks, len_task=len(tasks))
    else:
        return render_template('homework.html', tasks=tasks, len_task=0)


@app.route('/add_timetable', methods=['GET', 'POST'])
@login_required
def add_timetable():
    timetable_form = TimetableForm()
    if timetable_form.validate_on_submit():
        db = db_session.create_session()
        timetable = Timetable()
        timetable.lesson = timetable_form.lesson.data
        timetable.room = timetable_form.room.data
        timetable.begin = timetable_form.begin.data
        timetable.end = timetable_form.end.data
        timetable.day = timetable_form.day.data
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
        return redirect('/upload_file/<homework_form.file.data>')
    return render_template('add_homework.html', form=homework_form)


@app.route('/upload_file/<file>', methods=['GET', 'POST'])
@login_required
def upload_file(file):
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return redirect('/homework')


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
