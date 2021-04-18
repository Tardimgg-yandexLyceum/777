import argparse
import os
import threading

from flask import Flask, render_template, redirect, request, make_response
from flask_login import LoginManager, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

import ConfigReader
import get_local_ip
from data import salt_api, ConverterObj
from data.UserController import UserController
from data.__all_models import User
from flask_restful import Api
from data.DataBaseServer import DBServer, DataBase, user_resources
import HomeApi


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class CreateTaskForm(FlaskForm):
    job_title = StringField('Job title', validators=[DataRequired()])
    team_leader_id = StringField('Team Leader id', validators=[DataRequired()])
    work_size = StringField('Work Size', validators=[DataRequired()])
    Collaborators = StringField("Collaborators")
    is_job_finished = BooleanField("Is job finished")
    submit = SubmitField('Сохранить')


class MainForm(FlaskForm):
    add_task = SubmitField('Добавить задачу', validators=[DataRequired()])


app = Flask(__name__)
api = Api(app)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = DataBase.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/work_base_app', methods=['POST'])
def work_base_app():
    if request.method == 'POST':
        try:
            if request.form["btn"] == "entrance":
                print("go to login")
                return redirect("/login")
            elif request.form["btn"] == "registration":
                print("go to registration")
                return redirect("/registration")
            elif request.form["btn"] == "exit":
                print("leave session")
                logout_user()
                return redirect("/")

        except Exception as e:
            print(e)


@app.route('/', methods=['GET', 'POST'])
def start_app():
    return render_template("base.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user_bin = HomeApi.get_bin_user(form.email.data)
            if type(user_bin) is str:
                user = ConverterObj.decode(user_bin)
                if user and UserController.check_password(user, form.password.data):
                    login_user(user, remember=form.remember_me.data)
                    return redirect("/main")
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        except ConnectionError:
            return make_response("Server error", 500)

    return render_template('login.html', title='Авторизация', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        try:
            user_bin = HomeApi.get_bin_user(form.email.data)
            if type(user_bin) is str:
                user = ConverterObj.decode(user_bin)
                if user and UserController.check_password(user, form.password.data):
                    login_user(user, remember=form.remember_me.data)
                    return redirect("/main")
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        except ConnectionError:
            return make_response("Server error", 500)

    return render_template('login.html', title='Авторизация', form=form)


@app.route('/main', methods=['GET', 'POST'])
def main_view_controller():
    form = MainForm()
    if form.validate_on_submit():
        return redirect("/add_task")

    return render_template('main.html', title='Главная', form=form)


@app.route('/add_task', methods=['GET', 'POST'])
def add_task_controller():
    form = CreateTaskForm()
    if form.validate_on_submit():
        # save
        return redirect("/main")

    return render_template('add_task.html', title='Добавление задачи', form=form)


if __name__ == '__main__':
    app.register_blueprint(salt_api.blueprint)

    def add_test_user():
        parser = argparse.ArgumentParser()
        parser.add_argument('--test', action="store_true")

        args = parser.parse_args()
        if args.test:
            UserController.create_test_user()

    host_db = ConfigReader.readDataBaseHost()
    port_db = int(ConfigReader.readDataBasePort())
    threading.Thread(target=lambda: DBServer.start_server(host=host_db, port=port_db, func_start=add_test_user), daemon=True).start()

    host_web_app = ConfigReader.readWebApplicationHost()
    port_web_app = int(ConfigReader.readWebApplicationPort())
    if host_web_app == "local":
        app.run(port=port_web_app, host=get_local_ip.get_ip())
    else:
        app.run(port=port_web_app, host=host_web_app)
