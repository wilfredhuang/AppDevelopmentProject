from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateUserForm, LoginForm
import shelve, User

app = Flask(__name__)

# Main page
# Current is Login Page
@app.route('/')
def home():
    return render_template('home.html')


# Called when user successful logged in
# HF
@app.route('/users/<name>')
def users(name):
    return 'Test successful, name is {}'.format(name)


# Called when user press submit at main page
# Two methods, GET is called when website request the page
# There is POST request only when user click the submit button
# HF
@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm(request.form)

    # Validate only on a POST request
    if request.method == 'POST' and login_form.validate():
        # TODO
        # access storage and compare details

        # TODO
        # If correct, login

        # TODO
        # If wrong, Show feedback aka error

        # Test code below
        #user = request.form['name']

        user = login_form.username.data

        # TODO change this to logged in state
        return redirect(url_for('users', name=user))

    # Get request will be skipped to this

    return render_template('userLogin.html', form=login_form)



if __name__ == '__main__':
    app.run()