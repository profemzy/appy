from flask import Flask, render_template, request, session

from src.models.common.database import Database
from src.models.user import User

app = Flask(__name__)
app.secret_key = "Password@1$"


@app.route('/')
def test_method():
    return "Tested and Trusted!"


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login-validate', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
        email = session['email']
        user = User.get_by_email(email)
        return render_template("profile.html", name=user.name)
    else:
        session['email'] = None

    return render_template("profile.html", email=session['email'])


if __name__ == '__main__':
    app.run()
