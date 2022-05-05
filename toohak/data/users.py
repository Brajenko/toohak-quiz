import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin, AnonymousUserMixin

from werkzeug.security import generate_password_hash, check_password_hash


from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    """Класс пользователя для бд"""
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, nullable=True)
    points = sqlalchemy.Column(sqlalchemy.Float, nullable=False, default=0)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    
    quizes = orm.relation("Quiz", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Anonymous(AnonymousUserMixin):
    """Анонимный пользователь для фласк логина
    нужен для юзернейма и айди, без него ошибка при рендере хедера в шаблонах"""
    def __init__(self):
        self.id = 0
        self.username = 'Guest'