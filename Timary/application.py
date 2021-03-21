import os
from datetime import timedelta

from flask import Flask, render_template, redirect, url_for, make_response, jsonify, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from Timary.data import db_session
from Timary.data.models import User
from Timary.forms import RegisterForm, LoginForm, ChangeForm

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
    if form.validate_on_submit():
        if len(form.password.data) < 6:
            return render_template('register_and_login.html', title='Твоя профессия',
                                   form=form, form1=login_form,
                                   message="Пароль слишком короткий")
        if form.password.data.isdigit() or form.password.data.isalpha():
            return render_template('register_and_login.html', title='Твоя профессия',
                                   form=form, form1=login_form,
                                   message="Пароль должен содержать буквы и цифры")
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
            return render_template('register_and_login.html', form=form, form1=login_form, message="Такого пользователя не существует",
                                   title='Твоя профессия')
        if user.check_password(login_form.password.data):
            login_user(user, remember=True)
            return redirect('/user_info')
        else:
            return render_template('register_and_login.html', form=form, form1=login_form, message="Неправильный пароль", title='Твоя профессия')
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
