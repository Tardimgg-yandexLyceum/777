import os

from flask import Flask, render_template

import ConfigReader
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
def main():
    return render_template('DBView.html')


def start_server(host, port, func_start=lambda: None):
    app.register_blueprint(db_api.blueprint)
    api.add_resource(user_resources.UserListResource, ConfigReader.read_add_user_api_url())
    api.add_resource(user_resources.UserResource, ConfigReader.read_get_user_api_url())
    api.add_resource(bin_user_resources.BinUserResource, ConfigReader.read_get_bin_user_api_url())
    DataBase.global_init("bd/name.bd")
    # UserController.UserController().create_test_user()
    # app.run(port=8080, host='127.0.0.1')
    # func_start()
    app.run(port=port, host=host)
