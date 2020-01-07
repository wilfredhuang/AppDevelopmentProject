from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateUserForm, LoginForm, SignUpForm
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


@app.route('/login/<code>')
def logged_in(code):
    return 'Test successful, button pressed is {}'.format(code)


# Called when sign up button is clicked from the login page
# HF
# TODO Signup page
@app.route('/signup')
def sign_up():
    signup_form = SignUpForm(request.form)

    return render_template('signUp.html', form=signup_form)

# Called when user press submit at main page
# Two methods, GET is called when website request the page
# There is POST request only when user click the submit button
# HF
@app.route('/loginMenu', methods=['POST', 'GET'])
def loginMenu():
    login_form = LoginForm(request.form)

    # When a button is clicked
    if request.method == 'POST':
        btn_pressed = request.form['submit']

        # Login clicked
        # Validate only on a POST request
        if login_form.validate() and btn_pressed == "Login":
            user = login_form.username.data
            #return redirect(url_for('login', code=temp))

            # TODO
            # access storage and compare details

            # TODO
            # If correct, login

            # TODO
            # If wrong, Show feedback aka error
            return redirect(url_for('users', name=user))

        # Sign up clicked
        elif btn_pressed == "Sign Up":
            return redirect(url_for('sign_up'))

    # Get request will be skipped to this

    return render_template('userLogin.html', form=login_form)



if __name__ == '__main__':
    app.run()