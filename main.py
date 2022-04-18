from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        print(request.form['username'])
    return render_template('login_form.html')


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
