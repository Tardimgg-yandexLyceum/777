from data.__all_models import User
from data.DataBaseServer import DataBase
from werkzeug.security import generate_password_hash, check_password_hash


class UserController:
    def __init__(self):
        self.session = DataBase.create_session()

    def create_test_user(self):
        test_user = User()
        test_user.surname = "qwe"
        test_user.name = "asd"
        test_user.age = 10
        test_user.position = "sdf"
        test_user.speciality = "ghe"
        test_user.address = "isu"
        test_user.email = "qwe@qwe"
        self.set_password(test_user, "qwe")
        self.session.add(test_user)
        self.session.commit()

    @staticmethod
    def set_password(user: User, password: str):
        user.hashed_password = generate_password_hash(password)

    @staticmethod
    def check_password(user: User, password: str):
        return check_password_hash(user.hashed_password, password)
