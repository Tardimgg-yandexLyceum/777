from time import time

import jwt
import HomeApi
from data import ConverterObj
from data.__all_models import User
from flask import current_app as app
from data.DataBaseServer import DataBase
from werkzeug.security import generate_password_hash, check_password_hash


class UserController:

    @staticmethod
    def create_user(email, password, name='user', surname="user", confirmed=True):
        try:
            get_salt_response = HomeApi.add_random_salt_value(password)
            salt = get_salt_response['salt']
            hashed_password = UserController.get_hashed_password(get_salt_response['salt_value'])
        except ConnectionError:
            salt = ""
            hashed_password = UserController.get_hashed_password(password)
        HomeApi.add_user(email=email, hashed_password=hashed_password,
                         name=name, surname=surname, salt=salt, confirmed=confirmed)

    @staticmethod
    def create_test_user():
        UserController.create_user(
            email="qwe@qwe",
            password='qwe',
            name='asd',
            surname='qwe'
        )

    @staticmethod
    def changing_user(user_id, change_properties: dict):
        try:
            check_id = HomeApi.check_id(user_id)
            if check_id:
                if 'password' in change_properties:
                    get_salt_response = HomeApi.add_random_salt_value(change_properties['password'])
                    change_properties['hashed_password'] = UserController.get_hashed_password(
                        get_salt_response['salt_value'])
                    change_properties['salt'] = get_salt_response['salt']
                    del change_properties['password']
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
    def get_user_token(user_id, expires_in=600):
        return jwt.encode(
            {'id': user_id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_user_token(token):
        try:
            user_id = jwt.decode(token, app.config['SECRET_KEY'],
                                 algorithms=['HS256'])['id']
        except:
            return None
        return user_id

    class UseUserApi:

        @staticmethod
        def get_bin_user(email: str, user_id=None):
            str_user = HomeApi.get_bin_user(email, user_id)
            if type(str_user) is str:
                return ConverterObj.decode(str_user)
            return None

        @staticmethod
        def get_user(email: str, user_id=None):
            return HomeApi.get_user(email, user_id)

        @staticmethod
        def check_email(email: str):
            return HomeApi.check_email(email)["contains_value"]

        @staticmethod
        def check_id(user_id: int):
            return HomeApi.check_id(user_id)["contains_value"]

        @staticmethod
        def delete_user(user_id: int):
            return HomeApi.delete_user(user_id)
