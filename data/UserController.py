from time import time

import jwt
import HomeApi
from data.__all_models import User
from flask import current_app as app
from data.DataBaseServer import DataBase
from werkzeug.security import generate_password_hash, check_password_hash


class UserController:

    @staticmethod
    def create_user(email, password, age, name='user', surname="user"):
        try:
            get_salt_response = HomeApi.add_random_salt_value(password)
            salt = get_salt_response['salt']
            hashed_password = UserController.get_hashed_password(get_salt_response['salt_value'])
        except ConnectionError:
            salt = ""
            hashed_password = UserController.get_hashed_password(password)
        HomeApi.add_user(email=email, hashed_password=hashed_password,
                         name=name, surname=surname, age=age, salt=salt)

    @staticmethod
    def create_test_user():
        UserController.create_user(
            email="qwe@qwe",
            password='qwe',
            age=18,
            name='asd',
            surname='qwe'
        )

    @staticmethod
    def changing_user(user_id, change_properties: dict):
        try:
            check_id = HomeApi.check_id(user_id)
            if check_id:
                if 'password' in change_properties:
                    change_properties['password'] = UserController.get_hashed_password(change_properties['password'])
                HomeApi.changing_user_properties(user_id, change_properties)
        except ConnectionError:
            pass

    @staticmethod
    def set_password(user: User, password: str):
        user.hashed_password = generate_password_hash(password)

    @staticmethod
    def get_hashed_password(password: str):
        return generate_password_hash(password)

    @staticmethod
    def check_password(user: User, password: str):
        try:
            password = HomeApi.add_salt_value(password, user.salt)['salt_value']
            return check_password_hash(user.hashed_password, password)
        except ConnectionError:
            return False

    @staticmethod
    def get_reset_password_token(id, expires_in=600):
        return jwt.encode(
            {'reset_password': id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return None
        return User.query.get(id)

    class UseUserApi:

        @staticmethod
        def get_bin_user(email: str):
            HomeApi.get_bin_user(email)

        @staticmethod
        def get_user(email: str, user_id=None):
            HomeApi.get_user(email, user_id)

        @staticmethod
        def check_email(email: str):
            HomeApi.check_email(email)

        @staticmethod
        def check_id(user_id: int):
            HomeApi.check_id(user_id)



