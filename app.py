from flask import Flask, render_template, request, redirect, url_for, flash
from Forms import CreateUserForm, LoginForm, SignUpForm
import shelve, User
import main
import StorageManager as SM


app = Flask(__name__)
main.init()

# Main page
# Current is Login Page
@app.route('/')
def home():
    return render_template('home.html')


# Called For testing
# HF
@app.route('/testing/<code>')
def testing(code):
    return 'Test successful, code is {}'.format(code)


# Called when user successful logged in
# HF
@app.route('/users/<name>')
def users(name):
    return render_template('users.html')


# Called when sign up button is clicked from the login page
# HF
@app.route('/signup', methods=['POST', 'GET'])
def sign_up():
    signup_form = SignUpForm(request.form)
    if request.method == 'POST' and signup_form.validate():

        user = User.User(signup_form.first_name.data, signup_form.last_name.data, signup_form.username.data.lower(),
                         signup_form.password.data, signup_form.postal_code.data, signup_form.address.data,
                         signup_form.country.data, signup_form.city.data, signup_form.unit_number.data)

        # to create and check if the storage exist
        main.db.get_storage('Users', True, True)
        main.db.add_item('Users', user.get_username(), user)
        return redirect(url_for('users', name=user.get_username(), user_details=user))

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
            login_name = login_form.username.data.lower()
            #return redirect(url_for('login', code=temp))

            temp = main.db.return_keys("Users")

            if temp != None and login_name in temp:
                temp2 = main.db.get_storage("Users")
                user = temp2[login_name]
                return redirect(url_for('users', name=user.get_username(), user_details=user))

            else:
                print("ERRORRRRRR")


        # Sign up clicked
        elif btn_pressed == "Sign Up":
            return redirect(url_for('sign_up'))

    # Get request will be skipped to this

    return render_template('userLogin.html', form=login_form)



if __name__ == '__main__':
    app.run()