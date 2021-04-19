import HomeApi
from data.__all_models import User
from data.DataBaseServer import DataBase
from werkzeug.security import generate_password_hash, check_password_hash


class UserController:

    @staticmethod
    def create_user(email, password, age, name='user', surname="user"):
        session = DataBase.create_session()
        test_user = User()
        test_user.surname = surname
        test_user.name = name
        test_user.age = age
        test_user.email = email
        try:
            get_salt_response = HomeApi.add_random_salt_value(password)
            test_user.salt = get_salt_response['salt']
            UserController.set_password(test_user, get_salt_response['salt_value'])
        except ConnectionError:
            test_user.salt = ""
            UserController.set_password(test_user, password)
        session.add(test_user)
        session.commit()

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
    def check_password(user: User, password: str):
        try:
            password = HomeApi.add_salt_value(password, user.salt)['salt_value']
            return check_password_hash(user.hashed_password, password)
        except ConnectionError:
            return False
