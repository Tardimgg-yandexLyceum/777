import HomeApi
from data.__all_models import User
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
