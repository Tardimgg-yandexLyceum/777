from flask_restful import Resource, abort, reqparse
from flask import jsonify, request, make_response

import HomeApi
from data.UserController import UserController
from data.__all_models import User
from data.DataBaseServer import DataBase

parser = reqparse.RequestParser()
parser.add_argument('name', location="json", required=True)
parser.add_argument('surname', location="json", required=True)
parser.add_argument('age', location="json", required=True, type=int)
parser.add_argument('email', location="json", required=True)
parser.add_argument('hashed_password', location="json", required=True)
parser.add_argument('salt', location="json", required=True, type=list)


class UserResource(Resource):

    def get(self):
        if request.json:
            if 'email' in request.json:
                abort_if_user_not_found(request.json['email'])
                db_session = DataBase.create_session()
                email = request.json['email']
                user = db_session.query(User).filter(User.email == email).first()
                return jsonify(user.to_dict())
            elif 'id' in request.json:
                abort_if_user_not_found(email=None, user_id=request.json['id'])
                db_session = DataBase.create_session()
                user_id = request.json['id']
                user = db_session.query(User).filter(User.id == user_id).first()
                return jsonify(user.to_dict())
        else:
            return make_response(jsonify({'error': "No email in the request"}), 400)

    def post(self):
        if request.json and all(val in request.json for val in ("id", "change_properties")):
            abort_if_user_not_found(email=None, user_id=request.json['id'])
            db_session = DataBase.create_session()
            user = db_session.query(User).filter(User.id == request.json['id'])
            try:
                for param in request.json:
                    vars(user)[param] = request.json[param]
            except:
                abort(400, messgae='invalid value type')
            db_session.commit()
            return jsonify({'success': 'OK'})
        else:
            return make_response(jsonify({'error': "No email in the request"}), 400)

    def delete(self, news_id):
        abort_if_user_not_found(news_id)
        session = DataBase.create_session()
        news = session.query(User).get(news_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):

    def post(self):
        args = parser.parse_args()
        session = DataBase.create_session()
        test_user = User()
        test_user.name = args["name"]
        test_user.surname = args["surname"]
        test_user.age = args["age"]
        test_user.email = args["email"]
        test_user.hashed_password = args["hashed_password"]
        test_user.salt = args["salt"]
        session.add(test_user)
        session.commit()

        return jsonify({'success': 'OK'})


def abort_if_user_not_found(email, user_id=None):
    session = DataBase.create_session()
    if user_id:
        user = session.query(User).filter(User.id == user_id).first()
    else:
        user = session.query(User).filter(User.email == email).first()
    if not user:
        abort(404, message=f"User {email} not found")
