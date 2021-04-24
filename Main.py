import argparse
import os
import threading

from flask import Flask, render_template, redirect, request, make_response
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_mail import Mail
from wtforms import PasswordField, BooleanField, SubmitField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

import ConfigReader
import get_local_ip
from data import salt_api, ConverterObj, authorization, EMail_api
from data.UserController import UserController
from data.__all_models import User
from flask_restful import Api
from data.DataBaseServer import DBServer, DataBase, user_resources
import HomeApi


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

app.config['MAIL_SERVER'] = ConfigReader.read_mail_server()
app.config['MAIL_PORT'] = ConfigReader.read_mail_port()
app.config['MAIL_USE_TLS'] = ConfigReader.read_mail_use_tls()
app.config['MAIL_USERNAME'] = ConfigReader.read_mail_username()
app.config['MAIL_PASSWORD'] = ConfigReader.read_mail_password()
app.config['ADMINS'] = [ConfigReader.read_mail_admins()]
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return UserController.UseUserApi.get_bin_user(email="", user_id=user_id)


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
    form = MainForm()
    if form.validate_on_submit():
        return redirect("/add_task")

    return render_template('main.html', title='Главная', form=form)


if __name__ == '__main__':
    app.register_blueprint(salt_api.blueprint)
    app.register_blueprint(authorization.blueprint)
    app.register_blueprint(EMail_api.blueprint)


    def add_test_user():
        print("***************")
        parser = argparse.ArgumentParser()
        parser.add_argument('--test', action="store_true")

        args = parser.parse_args()
        if args.test:
            UserController.create_test_user()


    host_db = ConfigReader.read_data_base_host()
    port_db = int(ConfigReader.read_data_base_port())
    threading.Thread(target=lambda: DBServer.start_server(host=host_db, port=port_db, func_start=add_test_user),
                     daemon=True).start()

    host_web_app = ConfigReader.read_web_application_host()
    port_web_app = int(ConfigReader.read_web_application_port())
    if host_web_app == "local":
        app.run(port=port_web_app, host=get_local_ip.get_ip())
        # app.run(port=port_web_app, host="0.0.0.0")
    else:
        app.run(port=port_web_app, host=host_web_app)
