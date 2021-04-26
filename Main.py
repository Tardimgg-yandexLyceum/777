import os
import os
import threading
from time import time

from flask import Flask, render_template, redirect, request, url_for, session, jsonify
from flask_login import LoginManager, logout_user, current_user
from flask_mail import Mail
from flask_restful import Api
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.fields.html5 import IntegerField

import ConfigReader
import HomeApi
import get_local_ip
from data import salt_api, authorization, EMail_api, event_api, EventServer
from data.DataBaseServer import DBServer
from data.UserController import UserController


class MainForm(FlaskForm):
    pass


class EventForm(FlaskForm):
    selected_coef = StringField('Коэффициент', render_kw={'readonly': True})

    money = IntegerField('Ставка')
    submit = SubmitField('Поставить')


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

            translate = {
                "футбол": "football_mini.jpg",
                "волейбол": "volleyball_mini.png",
                "хоккей": "hockey_mini.png",
                "баскетбол": "basketball_mini.png"
            }
            event_img = translate[title.lower()]

            value['image'] = url_for('static', filename=f'image/{event_img}')
            value['redirect_first_event'] = f"/{title}/{value['first_event']}"
            value['redirect_second_event'] = f"/{title}/{value['second_event']}"
            value['redirect_third_event'] = f"/{title}/{value['third_event']}"
            value['redirect_event'] = f"/event/{title}"
            cards.append(value)

        background = url_for('static', filename='image/main_logo.png')

        return render_template('main.html', cards=cards, form=form, background=background)
    return redirect(f"/event{' '.join(request.form['btn'].split('_'))}")


@app.route('/event/<string:event_type>', methods=['GET', 'POST'])
def show_events(event_type):
    if request.method == 'GET':
        form = MainForm()
        data = HomeApi.get_all_events_by_type(event_type)
        titles = data['columns']

        translate = {
            "футбол": "football.png",
            "волейбол": "volleyball.png",
            "хоккей": "hockey.png",
            "баскетбол": "basketball.png"
        }
        link = translate[event_type.lower()]

        background = url_for('static', filename=f'image/{link}')

        events = []
        for key, value in data.items():
            if key != 'columns':
                vs = f"{value['team_1']} vs {value['team_2']}"
                value['coef'] = list(map(lambda x: float('{:.2f}'.format(x)), value['coef']))

                event = {
                    'event': vs,
                    'redirection': f"/event/{event_type}/{vs}",
                    'coef': value['coef']
                }
                events.append(event)

        return render_template('events.html', titles=titles, events=events, form=form, background=background)
    return redirect(" ".join(request.form['btn'].split("_")))


@app.route('/event/<string:event_type>/<string:event>', methods=['GET', 'POST'])
def show_event(event_type, event):
    form = EventForm()

    event = event.split()
    event[1] = "_"
    data = HomeApi.get_event(event_type, "".join(event))

    try:

        coef = list(map(lambda x: float('{:.2f}'.format(x)), data['1']['coef']))
    except Exception as e:
        return jsonify({
            "message": 'the competition is over'
        })

    vs = f"{data['1']['team_1']} vs {data['1']['team_2']}"
    time_end = data['1']['time']

    translate = {
        "футбол": "football",
        "волейбол": "volleyball",
        "хоккей": "hockey",
        "баскетбол": "basketball"
    }
    event_type = translate[event_type.lower()]

    background = url_for('static', filename=f'image/{event_type}.png')

    first = {
        'title': event[0],
        'image': f'{url_for("static", filename="")}image/{event_type}_clubs/{event[0]}.jpg'
    }
    second = {
        'title': event[2],
        'image': f'{url_for("static", filename="")}image/{event_type}_clubs/{event[2]}.jpg'
    }

    if 'submit' in request.form:
        if not request.form['selected_coef'] or not request.form['money'] or request.form['money'] == '0':
            return render_template('event.html', form=form, coef=coef, event=vs,
                                   team_1=first, team_2=second, time=f"До конца: {int(time_end - time())} c",
                                   titles=data['columns'], message="Нет ставки", background=background)
        if current_user.is_authenticated:
            budget = UserController.UseUserApi.get_user(email="", user_id=session["id"])['money']
            if budget >= int(request.form['money']):

                UserController.changing_user(session['id'], {
                    "money": budget - int(request.form['money'])
                })
                HomeApi.read_add_user_event(user_id=session['id'], money=request.form['money'],
                                            coef=request.form['selected_coef'], time=time_end)

                return render_template('event.html', form=form, coef=coef, event=vs,
                                       team_1=first, team_2=second, time=f"До конца: {int(time_end - time())} c",
                                       titles=data['columns'], message='Ставка создана', background=background)
            else:
                return render_template('event.html', form=form, coef=coef, event=vs,
                                       team_1=first, team_2=second, time=f"До конца: {int(time_end - time())} c",
                                       titles=data['columns'], message='Не хватает денег', background=background)
        else:
            return render_template('event.html', form=form, coef=coef, event=vs,
                                   team_1=first, team_2=second, time=f"До конца: {int(time_end - time())} c",
                                   titles=data['columns'], message='Вы не вошли в аккаунт', background=background)

    if request.method == 'GET':
        return render_template('event.html', form=form, coef=coef, event=vs,
                               team_1=first, team_2=second, time=f"До конца: {int(time_end - time())} c",
                               titles=data['columns'], background=background)

    selected_coef = coef[int(request.form['btn']) - 1]

    return render_template('event.html', form=form, coef=coef, event=vs,
                           team_1=first, team_2=second, time=f"До конца: {int(time_end - time())} c",
                           titles=data['columns'], selected_coef=selected_coef, background=background)


if __name__ == '__main__':
    app.register_blueprint(salt_api.blueprint)
    app.register_blueprint(authorization.blueprint)
    app.register_blueprint(EMail_api.blueprint)
    app.register_blueprint(event_api.blueprint)
    app.register_blueprint(EventServer.blueprint)

    host_db = ConfigReader.read_data_base_host()
    port_db = int(ConfigReader.read_data_base_port())
    threading.Thread(target=lambda: DBServer.start_server(host=host_db, port=port_db),
                     daemon=True).start()

    threading.Thread(target=EventServer.event_service,
                     daemon=True).start()

    host_web_app = ConfigReader.read_web_application_host()
    port_web_app = int(ConfigReader.read_web_application_port())
    if host_web_app == "local":
        app.run(port=port_web_app, host=get_local_ip.get_ip())
        # app.run(port=port_web_app, host="0.0.0.0")
    else:
        app.run(port=port_web_app, host=host_web_app)
