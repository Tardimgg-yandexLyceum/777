from flask_restful import Resource, abort, reqparse
from flask import jsonify, request, make_response

from data.__all_models import User
from data.DataBaseServer import DataBase

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('is_private', required=True, type=bool)
parser.add_argument('is_published', required=True, type=bool)
parser.add_argument('user_id', required=True, type=int)


class UserResource(Resource):

    def get(self):
        db_session = DataBase.create_session()
        if request.json and 'email' in request.json:
            email = request.json['email']
            abort_if_user_not_found(email)
            user = db_session.query(User).filter(User.email == email).first()
            return jsonify(user.to_dict())
        else:
            return make_response(jsonify({'error': "No email in the request"}), 400)

    def post(self):  # change properties
        pass

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
        user = User(
            title=args['title'],
            content=args['content'],
            user_id=args['user_id'],
            is_published=args['is_published'],
            is_private=args['is_private']
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_user_not_found(email):
    session = DataBase.create_session()
    user = session.query(User.email == email).first()
    if not user[0]:
        abort(404, message=f"User {email} not found")
