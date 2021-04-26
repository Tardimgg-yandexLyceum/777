from flask import jsonify, request, make_response
from flask_restful import Resource, abort

from data import ConverterObj
from data.DataBaseServer import DataBase
from data.__all_models import User


class BinUserResource(Resource):

    def get(self):
        db_session = DataBase.create_session()
        if request.json:
            if 'email' in request.json:
                email = request.json['email']
                abort_if_user_not_found(email)
                user = db_session.query(User).filter(User.email == email).first()
                return jsonify(ConverterObj.encode(user))
                # return make_response(jsonify({'error': "No user in the system"}))
            elif 'id' in request.json:
                user_id = request.json['id']
                abort_if_user_not_found(email=None, user_id=user_id)
                user = db_session.query(User).filter(User.id == user_id).first()
                return jsonify(ConverterObj.encode(user))
        else:
            return make_response(jsonify({'error': "No email in the request"}), 400)


def abort_if_user_not_found(email, user_id=None):
    session = DataBase.create_session()
    if user_id:
        user = session.query(User).filter(User.id == user_id).first()
    else:
        user = session.query(User).filter(User.email == email).first()
    if not user:
        abort(404, message=f"User {email} not found")
