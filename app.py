from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateUserForm
import shelve, User

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('userLogin.html')

@app.route('/users/<email>')
def users(email):
    return 'Test successful, email is {}'.format(email)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['email']
        return redirect(url_for('users', email=user))



if __name__ == '__main__':
    app.run()