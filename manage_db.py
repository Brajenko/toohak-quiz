from data.db_session import *
from data.users import User
from data.quizes import Quiz
from forms import RegisterForm, AddQuizForm


def add_new_user(form: RegisterForm):
    global_init("db/users.db")
    session = create_session()
    user = User()
    user.login = form.name.data
    user.email = form.email.data
    user.set_password(form.password.data)
    session.add(user)
    session.commit()


def get_user_by_id(user_id: str):
    return User.get(user_id)
    


def add_new_quiz(form: AddQuizForm):
    pass


def get_quiz_by_id(quiz_id: str):
    return Quiz.get(quiz_id)