import codecs

import flask
from flask import jsonify, make_response, request

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


@blueprint.route('/api/check_email', methods=['GET'])
def check_email_api():
    if request.json and 'email' in request.json:
        email = request.json['email']
        return jsonify({
            'contains_value': check_user(email)
        })
    else:
        return make_response(jsonify({'error': "No email in the request"}), 400)


def check_user(email: str):
    if request.json and 'email' in request.json:
        db_session = DataBase.create_session()
        user = db_session.query(User.email == email).first()
        return user[0]
    else:
        return False


@blueprint.route('/api/get_user', methods=['GET'])
def get_user():
    if request.json and 'email' in request.json:
        db_session = DataBase.create_session()
        email = request.json['email']
        if check_user(email):
            user = db_session.query(User).filter(User.email == email).first()
            return jsonify(ConverterObj.encode(user))
        return make_response(jsonify({'error': "No user in the system"}))
    else:
        return make_response(jsonify({'error': "No email in the request"}), 400)
