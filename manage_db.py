import json
from flask import session
from data.db_session import *
from data.users import User
from data.quizes import Quiz
from forms import RegisterForm, AddQuizForm


def add_new_user(form: RegisterForm) -> None:
    global_init("db/users.db")
    session = create_session()
    user = User()
    user.login = form.name.data
    user.email = form.email.data
    user.set_password(form.password.data)
    session.add(user)
    session.commit()


def get_user_by_id(user_id: str) -> User:
    global_init("db/users.db")
    session = create_session()
    return session.query(User).filter(User.id == int(user_id)).first()
    

def add_new_quiz(form: AddQuizForm, user) -> None:
    global_init("db/users.db")
    session = create_session()
    quiz = Quiz()
    quiz.name = form.name.data
    quiz.description = form.description.data
    # TODO: СДЕЛАТЬ ПОЛУЧЕНИЕ USER_ID
    quiz.creator = 0
    quiz.add_questions(form.questions.data)
    session.add(quiz)
    session.commit()

def get_quiz_by_id(quiz_id: str) -> Quiz:
    global_init("db/users.db")
    session = create_session()
    return session.query(Quiz).filter(Quiz.id == int(quiz_id)).first()


def add_new_completion(user_id, quiz_id):
    pass