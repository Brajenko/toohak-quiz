import json
from typing import List
from flask_login import UserMixin
from sqlalchemy import func
from toohak.data.db_session import *
from toohak.data.users import User
from toohak.data.completions import Completion
from toohak.data.quizes import Quiz
from toohak.forms import RegisterForm, AddQuizForm


def add_new_user(form: RegisterForm) -> None:
    """Добавить пользователя"""
    session = create_session()
    user = User()
    user.login = form.login.data
    user.email = form.email.data
    user.set_password(form.password.data)
    session.add(user)
    session.commit()


def get_user_by_id(user_id: str) -> User:
    """Получить пользователя по id"""
    session = create_session()
    return session.query(User).get(user_id)


def get_user_by_email(email:str) -> User:
    """Получить пользователя по емэйл"""
    session = create_session()
    return session.query(User).filter(User.email == email).first()


def get_user_by_login(login) -> User:
    """получить пользователя по логину"""
    session = create_session()
    return session.query(User).filter(User.login == login).first()


def increase_user_pts(user_id: int, n: int) -> None:
    """Добавить пользователю n очков в рейтинг"""
    session = create_session()
    user = session.query(User).get(user_id)
    user.points = user.points + float(n)
    session.commit()


def get_leaders() -> List[User]:
    """Получить список лидеров сайта"""
    session = create_session()
    return session.query(User).order_by(-User.points).limit(50).all()
    

def add_new_quiz(form: AddQuizForm, user: User) -> None:
    """Добавить новый тест
    переменная user - создатель теста"""
    session = create_session()
    quiz = Quiz()
    quiz.name = form.name.data
    quiz.description = form.description.data
    quiz.creator = user.get_id()
    quiz.add_questions(form.questions.data)
    session.add(quiz)
    session.commit()

def get_quiz_by_id(quiz_id: str) -> Quiz:
    """Получить тест по id"""
    session = create_session()
    return session.query(Quiz).filter(Quiz.id == int(quiz_id)).first()


def get_all_quizes_for_page(user_id, by_user=False) -> List[Quiz]:
    """Получить все тесты для главной страницы
    флаг by_user - получить для текущего/всех пользователей"""
    session = create_session()
    all_quizes = session.query(Quiz).join(User)
    if by_user:
        all_quizes = all_quizes.filter(User.id == user_id)
    out = []
    for quiz in all_quizes:
        max_compl = get_max_completion(user_id, quiz.id)
        out.append((quiz, max_compl))
    return out


def add_new_completion(user_id: int, quiz_id: int, score: int, percents: float):
    """Записать новую попытку после прохождения теста пользователем"""
    session = create_session()
    completion = Completion(user_id=user_id, quiz_id=quiz_id, score=score, percents=percents)
    session.add(completion)
    session.commit()


def get_completions(user_id, quiz_id):
    """Получить все прохождения теста пользователем по id"""
    session = create_session()
    return session.query(Completion).filter((Completion.user_id == user_id) & (Completion.quiz_id == quiz_id)).all()


def get_max_completion(user_id, quiz_id):
    """Получить лучшее прохождение теста пользователем по id"""
    session = create_session()
    return session.query(func.max(Completion.percents)).filter((Completion.user_id == user_id) & (Completion.quiz_id == quiz_id)).first()[0]