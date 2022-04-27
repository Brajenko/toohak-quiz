import json
import random
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


VARIANTS_IN_ROW = 4

class Quiz(SqlAlchemyBase):
    __tablename__ = 'quizes'
    
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    questions = sqlalchemy.Column(sqlalchemy.JSON, nullable=False)
    creator = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"), nullable=False)
    user = orm.relation('User')
    completions = orm.relation("Completion", back_populates='quiz')
    
    def get_questions(self):
        return json.loads(self.questions)

    def add_questions(self, json_questions):
        questions = json.loads(json_questions)
        for question in questions:
            all_variants = question['variants'] + [question['answer']]
            random.shuffle(all_variants)
            question['rows'] = [all_variants[i:i + VARIANTS_IN_ROW] for i in range(0, len(all_variants), VARIANTS_IN_ROW)]
            del question['variants']

        self.questions = json.dumps(questions)
