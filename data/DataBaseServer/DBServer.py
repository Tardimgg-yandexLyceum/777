import os

from flask import Flask, render_template

from data import UserController
from data.DataBaseServer import user_resources, DataBase
from data.DataBaseServer import bin_user_resources
from . import db_api
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/', methods=['GET', 'POST'])
def start_app():
    return render_template('DBView.html')


def start_server(host, port):
    app.register_blueprint(db_api.blueprint)
    api.add_resource(user_resources.UserListResource, '/api/usersProperties')
    api.add_resource(user_resources.UserResource, '/api/userProperties')
    api.add_resource(bin_user_resources.BinUserResource, '/api/user')
    DataBase.global_init("bd/name.bd")
    #UserController.UserController().create_test_user()
    #app.run(port=8080, host='127.0.0.1')
    app.run(port=port, host=host)
