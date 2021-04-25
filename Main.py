import argparse
import os
import threading

from flask import Flask, render_template, redirect, request, make_response, url_for
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_mail import Mail
from wtforms import PasswordField, BooleanField, SubmitField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

import ConfigReader
import get_local_ip
from data import salt_api, ConverterObj, authorization, EMail_api, event_api
from data.UserController import UserController
from data.__all_models import User
from flask_restful import Api
from data.DataBaseServer import DBServer, DataBase, user_resources
import HomeApi


class MainForm(FlaskForm):
    pass


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
            elif request.form["btn"] == "root":
                print("go to root")
                return redirect("/")
            elif request.form["btn"] == "exit":
                print("leave session")
                logout_user()
                return redirect("/")

        except Exception as e:
            print(e)


@app.route('/', methods=['GET', 'POST'])
def start_app():
    form = MainForm()
    if request.method == 'GET':

        data = HomeApi.get_main_events()
        cards = []

        for title, value in data.items():
            value['title'] = title
            value['image'] = url_for('static', filename='image/football_mini.jpg')
            value['redirect_first_event'] = f"{title}/{value['first_event']}"
            value['redirect_second_event'] = f"{title}/{value['second_event']}"
            value['redirect_third_event'] = f"{title}/{value['third_event']}"
            cards.append(value)

        return render_template('main.html', cards=cards, form=form)
    return redirect(" ".join(request.form['btn'].split("_")))


@app.route('/<string:event_type>', methods=['GET', 'POST'])
def show_events(event_type):
    if request.method == 'GET':
        form = MainForm()
        data = HomeApi.get_all_events_by_type(event_type)
        titles = data['columns']
        events = []
        for key, value in data.items():
            if key != 'columns':
                vs = f"{value['team_1']} vs {value['team_2']}"
                value['coef'] = list(map(lambda x: float('{:.2f}'.format(x)), value['coef']))

                event = {
                    'event': vs,
                    'redirect': f"{event_type}/{vs}",
                    'coef': value['coef']
                }
                events.append(event)

        return render_template('events.html', titles=titles, events=events, form=form)

    return redirect(" ".join(request.form['btn'].split("_")))


@app.route('/<string:event_type>/<string:event>', methods=['GET', 'POST'])
def show_event(event_type, event):
    return render_template('base.html')


if __name__ == '__main__':
    app.register_blueprint(salt_api.blueprint)
    app.register_blueprint(authorization.blueprint)
    app.register_blueprint(EMail_api.blueprint)
    app.register_blueprint(event_api.blueprint)


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
