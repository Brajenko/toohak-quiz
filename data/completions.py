import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Completion(SqlAlchemyBase):
    __tablename__ = 'completions'
    
    id = sqlalchemy.Column(sqlalchemy.Integer,
            primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"), nullable=False)
    quiz_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("quizes.id"), nullable=False)
    score = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    percents = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
    quiz = orm.relation('Quiz')
    user = orm.relation('User')