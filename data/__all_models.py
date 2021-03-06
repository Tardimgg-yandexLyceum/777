import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from data.DataBaseServer.DataBase import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    salt = sqlalchemy.Column(sqlalchemy.PickleType, nullable=True)
    confirmed = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=True)
    money = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=100)
