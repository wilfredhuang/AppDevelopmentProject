from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from Forms import CreateUserForm, LoginForm, SignUpForm, UserDetailsForm, ChangePasswordForm, AddressForm
from binascii import hexlify
import User, main, Product, os
#, paypalrestsdk, requests
import PasswordHashing

app = Flask(__name__)
SECRET_KEY = os.urandom(24)
app.secret_key = SECRET_KEY
main.init()

# Main page
# Current is Login Page
@app.route('/')
def home():
    return render_template('home.html')


# Called For testing
# HF
@app.route('/testing/<choice>')
def testing(choice):
    #return 'Test successful, code is {}'.format(code)
    return render_template('users.html')


# Called when user successful logged in
# HF
@app.route('/users/<username>/<int:choice>', methods=['POST', 'GET'])
def users(choice, username):
    # temp = main.db.return_keys("Users")
    username_list = main.user_management.get_username_list()

    user_form = UserDetailsForm(request.form)
    password_form = ChangePasswordForm(request.form)
    address_form = AddressForm(request.form)

    if request.method == 'POST':
        btn_pressed = request.form['submit']
        #user_db = main.user_management("Users")
        #user = user_db[username]
        user = main.user_management.get_user(username)

        if btn_pressed == "Update Profile" and user_form.validate():
            user.set_first_name(user_form.first_name.data)
            user.set_last_name(user_form.last_name.data)

            main.user_management.modify_user(user)
            flash('You have successfully updated profile')
            return redirect(url_for('users', choice=1, username=user.get_username()))
            #to_be_changed = main.db.get_storage("TEMP")
            #to_be_changed["username"] = user.get_username()

            #main.db.set_storage("TEMP", to_be_changed)

        elif btn_pressed == "Update Address" and address_form.validate():
            user.set_country(address_form.country.data)
            user.set_postal_code(address_form.postal_code.data)
            user.set_address(address_form.address.data)
            user.set_city(address_form.city.data)
            user.set_unit_number(address_form.unit_number.data)

            main.user_management.modify_user(user)
            flash('You have successfully updated address')
            return redirect(url_for('users', choice=1, username=user.get_username()))

        elif btn_pressed == "Change Password" and password_form.validate():
            hashed_password = PasswordHashing.hash_password(password_form.password.data)
            user.set_password(hashed_password)

            main.user_management.modify_user(user)
            flash('You have successfully changed password')
            return redirect(url_for('users', choice=1, username=user.get_username()))

    if username_list != None and username in username_list:

        #temp2 = main.db.get_storage("Users")
        #user_details = temp2[username]
        user_details = main.user_management.get_user(username)
        if choice == 1:
            temp_form = user_form
        elif choice == 2:
            temp_form = password_form
        elif choice == 3:
            temp_form = address_form

        return render_template('users.html', menu=choice, user=user_details, form=temp_form)

    else:
        print("ERRORRRRRR")




# Called when admin login
# HF
@app.route('/admin')
def admin():

    return render_template('admin.html')


# Called when sign up button is clicked from the login page
# HF
@app.route('/signup', methods=['POST', 'GET'])
def sign_up():
    signup_form = SignUpForm(request.form)
    if request.method == 'POST' and signup_form.validate():
        hashed_password = PasswordHashing.hash_password(signup_form.password.data)

        user = User.User(signup_form.first_name.data, signup_form.last_name.data, signup_form.username.data.lower(),
                         hashed_password, signup_form.postal_code.data, signup_form.address.data,
                         signup_form.country.data, signup_form.city.data, signup_form.unit_number.data)

        # to create and check if the storage exist - METHOD 1
        # main.db.get_storage('Users', True, True)
        # main.db.add_item('Users', user.get_username(), user)

        # Method 2
        main.user_management.add_user(user)

        # create temporary storage
        # main.db.get_storage("TEMP", True, True)
        # main.db.add_item('TEMP', "username", user.get_username())
        session['username'] = user.get_username()
        #main.session_management.add_item("username", user.get_username())

        return redirect(url_for('users', choice=1, username=user.get_username()))

    return render_template('signUp.html', form=signup_form)


# Called when user press submit at main page
# Two methods, GET is called when website request the page
# There is POST request only when user click the submit button
# HF
@app.route('/loginMenu', methods=['POST', 'GET'])
def loginMenu():
    login_form = LoginForm(request.form)

    # login if user already logged in before
   # temp_exist = main.storage_handler.storage_exist("TEMP")

    #if temp_exist == True:

       # session = main.storage_handler.get_storage("TEMP")
        #session_keys = main.session_management.get_keys()

        #if session_keys != None and "username" in session_keys:
            #username = session['username']
            #return redirect(url_for('users', choice=1, username=username))
    if 'username' in session:
        username = session['username']
        return redirect(url_for('users', choice=1, username=username))

    # When a button is clicked
    if request.method == 'POST':
        btn_pressed = request.form['submit']

        # Login clicked
        # Validate only on a POST request
        if login_form.validate() and btn_pressed == "Login":
            login_name = login_form.username.data.lower()

            #admin_acc = main.db.get_storage("ADMIN")
            admin_acc = main.storage_handler.get_storage("ADMIN")
            #temp = main.db.return_keys("Users")
            user_acc = main.user_management.get_username_list()

            if admin_acc.get_username() == login_name:
                print("Admin Login")
                return redirect(url_for('admin'))

            elif user_acc != None and login_name in user_acc:

                user = main.user_management.get_user(login_name)
                # main.session_management.add_item("username", user.get_username())
                session['username'] = user.get_username()
                return redirect(url_for('users', choice=1, username=user.get_username()))

            else:
                print("ERRORRRRRR")


        # Sign up clicked
        elif btn_pressed == "Sign Up":
            return redirect(url_for('sign_up'))

    # Get request will be skipped to this

    return render_template('userLogin.html', form=login_form)


# Figuring out carting system
# JH
# STILL TESTING
@app.route("/testAddItem", methods=["GET", "POST"])
def testAddItem():

    if request.method == "POST":
        if request.form["submit_button"] == "Add":
            # Create the product object
            product = Product.Product(1, "Airpods", 239.00)
            product2 = Product.Product(2, "Airpods Pro", 329.00)
            productList = []
            productList.append(product)
            productList.append(product2)
            # Add it into the database
            main.db.get_storage("Cart", True, True)
            main.db.update_cart("Cart", "TestUser", productList)
            print("-- TEST --")
            test = main.db.return_object("Cart")
            test = test["TestUser"]
            # print(f"Product Name: {test.get_name()}, Cost: {test.get_cost()}, ID: {test.get_id()}")
            print(test[0].get_name())
            print(test[1].get_name())
            print("-- TEST --")
        elif request.form["submit_button"] == "Delete":
            print("Delete item button pressed")
            main.db.get_storage("Cart", True, True)
            main.db.delete_storage("Cart")
    return render_template("test.html")


# Shopping cart page
# JH
# STILL TESTING
@app.route("/cart", methods=["GET", "POST"])
def cart():
    total_cost = 0
    if request.method == "POST":
        try:
            item = main.db.return_object("Cart")
            item = item["TestUser"]
            if request.form["cart_button"][0] == "+":
                print("---TEST---")
                print(item)
                for i in item:
                    if i.get_name() == request.form["cart_button"][1::]:
                        print(request.form["cart_button"][1::])
                        print(f"Item name: {i.get_name}, quantity: {i.get_quantity()}")
                        i.add_quantity()
                        print(f"Item name: {i.get_name}, quantity: {i.get_quantity()}")
                        main.db.delete_storage("Cart")
                        main.db.get_storage("Cart", True, True)
                        main.db.add_item("Cart", "TestUser", item)
                print("---TEST---")
            elif request.form["cart_button"][0] == "-":
                print("---TEST---")
                print(item)
                for i in item:
                    if i.get_name() == request.form["cart_button"][1::]:
                        print("test")
                        index = item.index(i)
                        item.pop(index)
                        main.db.delete_storage("Cart")
                        main.db.get_storage("Cart", True, True)
                        main.db.add_item("Cart", "TestUser", item)
                print("---TEST---")
            # Get total cost
            for i in item:
                total_cost += float(i.get_cost()) * float(i.get_quantity())
        except:
            pass



    main.db.get_storage("Cart", True, True)
    product_object = main.db.return_object("Cart")
    try:
        product_object = product_object["TestUser"]
    except:
        product_object = {}
    return render_template("userCart.html", item=product_object, total_cost=total_cost)

# Checkout options
# JH
@app.route("/checkoutoptions")
def checkout_options():
    return render_template("checkout_options.html")


# Guest Checkout
# JH
@app.route("/guestcheckout", methods=["GET", "POST"])
def guest_checkout():
    return render_template("g_checkout.html")

# Logged In Checkout - TESTING ONLY, NOT FINAL!!!!!
# JH
@app.route("/usercheckout", methods=["GET", "POST"])
def user_checkout():
    main.db.get_storage("Users", True, True)
    user = main.db.return_object("Users")
    user = user["tristan"]
    return render_template("u_checkout.html", user=user)

"""
# Payment page to enter card detail if not yet so
# JH
@app.route("/payment")
def payment():
    return render_template("payment_checkout.html")


# Show state of payment
# JH
@app.route("/paymentstate")
def payment_state():
    return render_template("paymentsuccess.html")


paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AdH9TKto-i55A59_fTE_EBenlB2BzMI7-Jn7nj6q31HwAdnFXObvrNuGs8m3CjIZBCqXnkK2EbwdFx3E",
  "client_secret": "EHwkI3DR_UEWZpjwksQ_TmeLYAswAAhl3CVDhSt9czUYOK59xMTH917nDlw8MXItNc0KL3Xv7tB3TndP"})


# paypal testing
# JH
@app.route("/paypaltest")
def paypal_test():
    return render_template("paypal_test.html")


# paypal testing
# JH
@app.route("/paypalpayment", methods=["POST"])
def paypalpayment():
    item_list = []
    total_cost = 0
    # Get cart
    item = main.db.return_object("Cart")
    item = item["TestUser"]
    for i in item:
        item_list.append({"name": i.get_name(),
                          "sku": "1",
                          "price": i.get_cost(),
                          "currency": "SGD",
                          "quantity": "1"})
        total_cost += float(i.get_cost()) * float(i.get_quantity())

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "item_list": {
                "items": item_list},
            "amount": {
                "total": total_cost,
                "currency": "SGD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print("Payment Success!")
    else:
        print("error here")
        print(payment.error)

    return jsonify({'paymentID': payment.id})


@app.route("/execute", methods=["POST"])
def execute():
    success = False
    payment = paypalrestsdk.Payment.find(request.form["paymentID"])

    if payment.execute({"payer_id": request.form["payerID"]}):
        print("Execute Sucess!")
        success = True
    else:
        print(payment.error)

    return jsonify({"success": success})

"""
if __name__ == '__main__':
    app.run()