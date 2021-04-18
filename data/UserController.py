import HomeApi
from data.__all_models import User
from data.DataBaseServer import DataBase
from werkzeug.security import generate_password_hash, check_password_hash


class UserController:

    @staticmethod
    def create_test_user():
        session = DataBase.create_session()
        test_user = User()
        test_user.surname = "qwe"
        test_user.name = "asd"
        test_user.age = 10
        test_user.position = "sdf"
        test_user.speciality = "ghe"
        test_user.address = "isu"
        test_user.email = "qwe@qwe"
        try:
            get_salt_response = HomeApi.add_random_salt_value('qwe')
            test_user.salt = get_salt_response['salt']
            UserController.set_password(test_user, get_salt_response['salt_value'])
        except ConnectionError:
            test_user.salt = ""
            UserController.set_password(test_user, "qwe")
        session.add(test_user)
        session.commit()

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
