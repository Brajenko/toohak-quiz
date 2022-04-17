from flask import Flask
from flask import render_template, request


app = Flask(__name__)

answers = [2, 4, 0]
questions=[{'type': 'variants',
            'text': 'Сколько ног у человека?',
            'rows': ((1, 2), (3, 4), (5, 6))},
           
           {'type': 'variants',
            'text': 'Сколько ног у кота?',
            'rows': ((1, 2), (3, 4))},
           
           {'type': 'variants',
            'text': 'Сколько ног у рыбы?',
            'rows': ((0, 1), (2, 1000))}]


curr_q = None
score = 0

@app.route('/', methods=['POST', 'GET'])
def index():
    global curr_q, score
    if request.method == 'POST':
        if str(answers.pop(0)) == request.form["answer"]:
            score += 1
        print(f'FORM: {request.form["answer"]}', file=open('forms.log', mode='a'))
        try:
            curr_q = questions.pop(0)
        except IndexError:
            return render_template('results.html', res=score)
        return render_template('quiz.html', question=curr_q)
    if request.method == 'GET':
        try:
            curr_q = questions.pop(0)
        except IndexError:
            return 'Вы уже прошли квест'
        return render_template('quiz.html', question=curr_q)


if __name__ == "__main__":
    app.run(debug=True)