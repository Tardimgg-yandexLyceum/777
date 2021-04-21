import codecs

import flask
from flask import jsonify, make_response, request

import ConfigReader
from data import ConverterObj
from . import DataBase
from data.__all_models import User

blueprint = flask.Blueprint(
    'db_api',
    __name__,

)


@blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@blueprint.route(ConfigReader.read_check_email_api_url(), methods=['GET'])
def check_email_api():
    if request.json and 'email' in request.json:
        email = request.json['email']
        db_session = DataBase.create_session()
        user = db_session.query(User).filter(User.email == email).first()
        return jsonify({
            'contains_value': True if user else False
        })
    else:
        return make_response(jsonify({'error': "No email in the request"}), 400)
