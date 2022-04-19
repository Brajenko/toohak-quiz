from flask import Flask, make_response, redirect, render_template, request
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)

from manage_db import (add_new_quiz, add_new_user, get_quiz_by_id,
                       get_user_by_id)

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = '0'


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    # TODO: написать обработчик регистраций
    add_new_user("СЮДА НУЖНА ФОРМА")
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # TODO: написать обработчик регистраций
    get_user_by_id("СЮДА ID ПОЛЬЗОВАТЕЛЯ")
    login_user("СЮДА ПОЛЬЗОВАТЕЛЯ")
    

@app.route('/account', methods=['GET', 'POST'])
def account():
    # TODO: сделать отображение данных аккаунта, реализовать их изменение (логин, пароль почта)
    pass


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@login_required
@app.route('/quiz/start/<int: id>')
def start_quiz(id):
    resp = make_response("")
    resp.set_cookie('quiz', id, 60 * 60)
    resp.set_cookie('question', 0, 60 * 60)
    return redirect('quiz')


@login_required
@app.route('/quiz')
def quiz():
    pass
    # Это пока не работает
    # if request.cookies.get('quiz') == 0:
    #     return redirect('/')
    
    # curr_quiz = get_quiz_by_id(request.cookies.get('quiz')).questions
    # if request.method == 'POST':
    #     if  == request.form["answer"]:
    #         score += 1
    #     try:
    #         curr_q = questions.pop(0)
    #     except IndexError:
    #         return render_template('results.html', res=score)
    #     return render_template('quiz.html', question=curr_q)
    # if request.method == 'GET':
    #     try:
    #         curr_q = questions.pop(0)
    #     except IndexError:
    #         return 'Вы уже прошли квест'
    #     return render_template('quiz.html', question=curr_q)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
