import os
import uuid
from datetime import date

import pandas as pd
import paypalrestsdk
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session

import Item
import Product
import User
from Forms import *

UPLOAD_FOLDER = 'static/files'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
SECRET_KEY = os.urandom(24)
app.secret_key = SECRET_KEY
main.init()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Hieu
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Hieu
def retrieveFiles():
    entries = os.listdir(app.config['UPLOAD_FOLDER'])
    fileList = []
    for entry in entries:
        fileList.append(entry)
    return fileList


# Main page / Homepage
@app.route('/')
def home():
    itemDict = main.get_inventory().values()
    ItemList = []
    for i in itemDict:
        ItemList.append(i)
    print(ItemList)
    return render_template('home.html', ItemList=ItemList)


# Google Analytics
# HF
@app.route('/ga_main', methods=['POST', 'GET'])
def ga_main():
    return render_template('googleAnalyticsAPI-Main.html')


# Google Analytics
# HF
@app.route('/ga_2', methods=['POST', 'GET'])
def ga_2():
    ac = main.get_access_token()
    return render_template('googleAnalyticsAPI2.html', ACCESS_TOKEN_FROM_SERVICE_ACCOUNT=ac)


# Google Analytics
# HF
@app.route('/ga_ssa', methods=['POST', 'GET'])
def ga_ssa():
    return render_template('googleAnalyticsAPI3-SSA.html')


# Called when user successful logged in
# HF
@app.route('/users/<username>/<int:choice>', methods=['POST', 'GET'])
def users(choice, username):
    username_list = main.user_management.get_username_list()

    # Forms for changing user's details
    user_form = UserDetailsForm(request.form)
    password_form = ChangePasswordForm(request.form)
    address_form = AddressForm(request.form)

    # When any of the details are updated
    if request.method == 'POST':
        btn_pressed = request.form['submit']

        # Get user obj
        user = main.user_management.get_user(username)

        # Check which form is being updated
        if btn_pressed == "Update Profile" and user_form.validate():

            # Update user obj details
            user.set_first_name(user_form.first_name.data)
            user.set_last_name(user_form.last_name.data)

            main.user_management.modify_user(user)

            # Feedback to know it has updated
            flash('You have successfully updated profile')

            return redirect(url_for('users', choice=1, username=user.get_username()))

        elif btn_pressed == "Update Address" and address_form.validate():

            # Update user obj details
            user.set_country(address_form.country.data)
            user.set_postal_code(address_form.postal_code.data)
            user.set_address(address_form.address.data)
            user.set_city(address_form.city.data)
            user.set_unit_number(address_form.unit_number.data)

            # Update persistent storage
            main.user_management.modify_user(user)

            # Feedback to know it has updated
            flash('You have successfully updated address')
            return redirect(url_for('users', choice=1, username=user.get_username()))

        elif btn_pressed == "Change Password" and password_form.validate():

            # store hashed password instead of plain text
            hashed_password = PasswordHashing.hash_password(password_form.password.data)

            # Update user obj details
            user.set_password(hashed_password)

            # Update persistent storage
            main.user_management.modify_user(user)

            # Feedback to know it has updated
            flash('You have successfully changed password')
            return redirect(url_for('users', choice=1, username=user.get_username()))

    # Prepare things needed for the page
    if username_list != None and username in username_list:

        user_details = main.user_management.get_user(username)

        # To see which panel user is at

        if choice == 1:
            temp_form = user_form
        elif choice == 2:
            temp_form = password_form
        elif choice == 3:
            temp_form = address_form

        return render_template('users.html', menu=choice, user=user_details, form=temp_form)

    else:
        print("ERRORRRRRR")


# Called after admin login
# HF & Hieu
@app.route('/admin')
def admin():
    user_list = main.storage_handler.get_storage("Users")
    inventory = main.get_inventory()
    wireless = []
    wired = []
    for i in inventory.values():
        if i.get_type() == 'W':
            wired.append(i)
        elif i.get_type() == 'WL':
            wireless.append(i)
        else:
            continue

    return render_template('admin.html', ItemList=inventory.values(), alarm_stock=10, wired=len(wired), wireless=len(wireless),userList=user_list, count=len(user_list))


# Sales
# HF
@app.route('/sales', methods=['POST', 'GET'])
def sales():
    sales_date_form = SalesForm(request.form)
    temp_sales = None
    if request.method == "POST":

        temp_sales = main.sales_management.get_report(int(sales_date_form.day.data), int(sales_date_form.month.data),
                                                      int(sales_date_form.year.data))

    return render_template('sales.html', form=sales_date_form, sales=temp_sales)


# Called when sign up button is clicked from the login page
# HF
@app.route('/signup', methods=['POST', 'GET'])
def sign_up():
    # Prepare form
    signup_form = SignUpForm(request.form)

    # Validate all input
    if request.method == 'POST' and signup_form.validate():
        # hash the password instead of leaving in plain text
        hashed_password = PasswordHashing.hash_password(signup_form.password.data)

        # create user obj
        user = User.User(signup_form.first_name.data, signup_form.last_name.data, signup_form.username.data.lower(),
                         hashed_password, signup_form.postal_code.data, signup_form.address.data,
                         signup_form.country.data, signup_form.city.data, signup_form.unit_number.data)

        # Store in persistent storage
        main.user_management.add_user(user)

        # add session storage, user will be logged in until logout is pressed or session ended
        session['username'] = user.get_username()

        # login
        return redirect(url_for('users', choice=1, username=user.get_username()))

    return render_template('signUp.html', form=signup_form)


# Called when user press submit at main page
# GET is called when website request the page
# There is POST request only when user click the submit button
# HF
@app.route('/loginMenu', methods=['POST', 'GET'])
def loginMenu():
    # Prepare form
    login_form = LoginForm(request.form)

    # login if user already logged in before in the session

    if 'username' in session:
        admin_acc = main.storage_handler.get_storage("ADMIN")
        username = session['username']
        if admin_acc.get_username() == username:
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('users', choice=1, username=username))

    # When a button is clicked
    if request.method == 'POST':
        btn_pressed = request.form['submit']

        # Login clicked
        # Validate only on a POST request
        if login_form.validate() and btn_pressed == "Login":

            login_name = login_form.username.data.lower()

            # get account list
            admin_acc = main.storage_handler.get_storage("ADMIN")
            user_acc = main.user_management.get_username_list()

            if admin_acc.get_username() == login_name:
                print("Admin Login")
                session['username'] = admin_acc.get_username()
                return redirect(url_for('admin'))

            elif user_acc != None and login_name in user_acc:

                user = main.user_management.get_user(login_name)
                session['username'] = user.get_username()
                return redirect(url_for('users', choice=1, username=user.get_username()))

            else:
                print("ERRORRRRRR")


        # Sign up clicked
        elif btn_pressed == "Sign Up":
            return redirect(url_for('sign_up'))

    # Get request will be skipped to this
    return render_template('userLogin.html', form=login_form)


# HF
# set to logged out and redirect to login page
@app.route("/SignOut")
def SignOut():
    del session['username']
    return redirect(url_for('loginMenu'))


# HF
# admin's user handling page
@app.route("/AdminUserDashboard")
def AdminUserDashboard():
    user_list = main.storage_handler.get_storage("Users")

    return render_template('AdminUserDashboard.html', userList=user_list, count=len(user_list))


# HF
# when user want to delete user from user handling page
@app.route('/deleteUser/<username>', methods=['POST'])
def deleteUser(username):
    main.user_management.delete_user(username)

    return redirect(url_for('AdminUserDashboard'))


# Debug page
# JH
@app.route("/testAddItem", methods=["GET", "POST"])
def testAddItem():
    # add any testcodes here
    return render_template("test.html")


# Shopping cart page
# JH
@app.route("/cart", methods=["GET", "POST"])
def cart():
    username = ""
    if 'username' in session:
        username = session['username']

    u_cart = main.cart_management.retrieve_cart(username)
    if request.method == "POST":
        # Add quantity
        if request.form["cart_button"][0] == "+":
            main.cart_management.cart_quantity(username, request.form["cart_button"][1::], "add")
        # Remove quantity
        elif request.form["cart_button"][0] == "-":
            main.cart_management.cart_quantity(username, request.form["cart_button"][1::], "remove")

    # Get total cost
    total_cost = 0
    for i in u_cart:
        total_cost += float(i.get_cost()) * float(i.get_quantity())

    # No checkout with empty cart
    cart_empty = False
    if len(u_cart) < 1:
        cart_empty = True

    return render_template("userCart.html", item=u_cart, total_cost=total_cost, cart_empty=cart_empty)


# Checkout options
# JH
@app.route("/checkoutoptions")
def checkout_options():
    return render_template("checkout_options.html")


# Guest Checkout
# JH
@app.route("/guestcheckout", methods=["GET", "POST"])
def guest_checkout():
    form = CheckoutForm(request.form)
    if request.method == "POST" and form.validate():
        data = []
        data.append(form.full_name.data + "," + form.address.data + "," + form.postal_code.data + "," + form.unit_number.data)
        data.append(form.countries.data)
        main.db.get_storage("temp_paypal", True, True)
        main.db.update_cart("temp_paypal", "paypal", data)
        return redirect(url_for('payment'))
    username = ""
    logged_in = False
    if 'username' in session:
        username = session['username']
        user = main.user_management.get_user(username)
        logged_in = True
        return render_template("g_checkout.html", form=form, user=user, logged_in=logged_in)
    else:
        return render_template("g_checkout.html", form=form)


# Logged In Checkout - TESTING ONLY, NOT FINAL!!!!!
# JH
@app.route("/usercheckout", methods=["GET", "POST"])
def user_checkout():
    username = ""
    if 'username' in session:
        username = session['username']
    main.db.get_storage("Users", True, True)
    user = main.db.return_object("Users")
    user = user[username]
    return render_template("u_checkout.html", user=user)


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
    "mode": "sandbox",  # sandbox or live
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
    username = ""
    if 'username' in session:
        username = session['username']
    data = main.db.return_object("temp_paypal")
    data = data["paypal"]  # 0: address, 1:country code
    # ----------
    item_list = []
    total_cost = 0
    # Get cart
    u_cart = main.cart_management.retrieve_cart(username)
    main.product_management.purchase_item(u_cart)
    for i in u_cart:
        item_list.append({"name": i.get_name(),
                          "sku": "1",
                          "price": i.get_cost(),
                          "currency": "SGD",
                          "quantity": i.get_quantity()})
        total_cost += float(i.get_cost()) * float(i.get_quantity())
    # Shipping Costs
    item_list.append({"name": "Shipping Costs",
                      "sku": "69",
                      "price": 5.99,
                      "currency": "SGD",
                      "quantity": "1"})
    total_cost += 5.99
    # Create Order details
    order_list = []
    try:
        main.db.get_storage("Order", True, True)
        orders = main.db.return_object("Order")
        order_list = orders["allorders"]
    except:
        main.db.get_storage("Order", True, True)
        main.db.update_cart("Order", "allorders", order_list)
        orders = main.db.return_object("Order")
        order_list = orders["allorders"]
    today = date.today()
    # new_order = Order.Order(u_cart, total_cost, data[0], "0", username, today)
    main.order_management.create_new_order(u_cart, total_cost, data[0], 0, username, today)
    # order_list.append(new_order)
    # main.db.update_cart("Order", "allorders", order_list)
    print("-----HELLO BODOH-------")
    print(order_list)
    # print(new_order)
    print("---------BYE BODOH-------")
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"
        },
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


# JH
@app.route("/execute", methods=["POST"])
def execute():
    username = ""
    if 'username' in session:
        username = session['username']
    # productList = []
    print(f"{username} THIS IS EXECUTE CODE")
    success = False
    payment = paypalrestsdk.Payment.find(request.form["paymentID"])
    if payment.execute({"payer_id": request.form["payerID"]}):
        print("Execute Sucess!")
        print(payment.amount)
        # main.db.update_cart("Cart", username, productList)
        main.cart_management.clear_cart_debug(username)
        success = True
    else:
        print(payment.error)

    return jsonify({"success": success})


# Feedback form
# Matt
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        print(request.form['message'])
        main.db.get_storage('feedback', True, True)
        main.db.update_cart('feedback', 'testfeedback', request.form['message'])
        return redirect(url_for('home'))

    if request.method == 'GET':
        try:
            feedback = main.db.return_object('feedback')
            feedback = feedback['testfeedback']
            print("This is the user feedback")
            print(feedback)
        except:
            print("There is no feedback")

    return render_template("feedback.html")


# Link to aboutUs
# Matt
@app.route("/aboutUs")
def aboutUs():
    return render_template("aboutUs.html")


# Hieu
@app.route('/adminItemDashboard', methods=['Get', 'Post'])
def adminItemDashboard():
    inventory = main.get_inventory().values()
    search_function = SearchForm(request.form)
    key = ""
    if request.method == 'POST':
        key = search_function.search.data
    print(f'key is {key}')

    return render_template('adminItemDashboard.html', ItemList=inventory, input=search_function,
                           key_search=key, alarm_stock=10)


# Hieu
@app.route('/createItem', methods=['Get', 'Post'])
def addItem():
    item = main.get_inventory()
    createItemForm = CreateItemForm(request.form)
    if request.method == 'POST':
        try:

            filename = str(uuid.uuid4()) + createItemForm.item_id.data + '.jpg'

            cost = float(f'{createItemForm.item_cost.data :.2f}')

            if createItemForm.item_type.data == "W":
                item = Item.Wired(createItemForm.item_id.data, createItemForm.item_name.data, cost,
                                  filename)
            elif createItemForm.item_type.data == "WL":
                item = Item.Wireless(createItemForm.item_id.data, createItemForm.item_name.data,
                                     cost, filename)

            item.set_description(createItemForm.item_description.data)
            item.set_stock(createItemForm.item_quantity.data)
            main.product_management.update_item(item)

            print(request.files)
            print(request.files['file'])
            print(filename)

            file = request.files['file']
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return redirect(url_for('adminItemDashboard'))
        except:
            print("Error")
            return render_template('adminCreateItem.html', form=createItemForm, errorMsg='Please enter valid values!')
    else:
        url_for('addItem', form=createItemForm)
    return render_template('adminCreateItem.html', form=createItemForm)


# Hieu
@app.route('/addItemExcel', methods=['GET', 'POST'])
def addItemExcel():
    inventory = main.get_inventory()
    if request.method == 'POST':
        try:
            file = request.files['file']
            data = pd.read_excel(file)  # read the file

            for i in range(len(data.index.values)):
                id = data['ID'][i]
                name = data['Name'][i]
                cost = data['Cost'][i]
                stock = data['Stock'][i]
                description = data['Description'][i]
                image = 'default_img.jpeg'
                type = data['Type'][i]  # to determine the type of product for sorting purpose

                wired = ['w', 'wired', 'W', 'Wired']
                wireless = ['wl', 'wireless', 'Wl', 'Wireless', 'WL']

                if type in wired:
                    item = Item.Wired(id, name, cost, image)
                elif type in wireless:
                    item = Item.Wireless(id, name, cost, image)



                if item.get_id() in inventory:
                    print('existing item. updating stock.')
                    existing_item = inventory[item.get_id()]
                    new_stock = existing_item.get_stock() + stock
                    print(new_stock)
                    existing_item.set_stock(new_stock)
                    print(existing_item.get_stock())
                    item.set_description(description)

                    main.product_management.modify_product(existing_item)

                else:
                    item.set_stock(stock)
                    item.set_description(description)
                    main.product_management.update_item(item)
            return redirect(url_for('adminItemDashboard'))
        except:
            return redirect(url_for('addItem'))
    return redirect(url_for('addItem'))


# Hieu
@app.route('/removeItem/<id>', methods=['POST'])
def removeItem(id):
    inventory = main.get_inventory()
    removedItem = inventory[id]
    if removedItem.get_file() is not 'default_img.jpeg':
        try:
            os.remove(f'files/{removedItem.get_file()}')
        except:
            print('error. file not found')
    else:
        pass

    main.product_management.delete_item(removedItem.get_id())

    return redirect(url_for('adminItemDashboard'))


# Hieu
@app.route('/updateItem/<id>', methods=['GET', 'POST'])
def updateItem(id):
    inventory = main.get_inventory()
    updateItemForm = CreateItemForm(request.form)
    if request.method == 'POST' and updateItemForm.validate():

        item = inventory.get(id)

        item.set_id(updateItemForm.item_id.data)
        item.set_name(updateItemForm.item_name.data)
        item.set_cost(updateItemForm.item_cost.data)
        item.set_stock(updateItemForm.item_quantity.data)
        item.set_description(updateItemForm.item_description.data)

        main.product_management.modify_product(item)

        return redirect(url_for('adminItemDashboard'))

    else:

        item = inventory.get(id)
        updateItemForm.item_id.data = item.get_id()
        updateItemForm.item_name.data = item.get_name()
        updateItemForm.item_quantity.data = item.get_stock()
        updateItemForm.item_cost.data = item.get_cost()
        updateItemForm.item_type.data = item.get_type()



        return render_template('adminUpdateItem.html', form=updateItemForm)


@app.route('/productDisplay', methods=["POST", "GET"])
def productDisplay():
    inventory = main.get_inventory().values()

    username = ""
    if "username" in session:
        username = session["username"]
    if request.method == 'POST':
        product_info = request.form["item_button"].split(",")  # List 0 = ID, 1 = Name, 2 = Price
        product = Product.Product(product_info[0], product_info[1], float(product_info[2]))
        main.cart_management.add_to_cart(username, product)

    return render_template('productDisplay.html', ItemList=inventory, username=username)


# Wilfred's delivery section

@app.route('/trackorders')
def trackorders():
    # user's order database should be retrieved here - W
    username = ""
    if 'username' in session:
        username = session['username']
    displayed_orders = {} #to be used for display in track orders page
    test = main.order_management.retrieve_all_order_id()
    the_user_orders = {} # This will contain the individual user's orders.
    the_user_order_count = 1 # Store each order with the count as key for sorting.
    for i in test:
        eachorder = main.order_management.retrieve_order_by_id(i)
        print("Object {}".format(eachorder))
        if eachorder.get_username() == username:
            the_user_orders[the_user_order_count] = eachorder
            the_user_order_count += 1
        else:
            pass
    sort_user_orders = sorted(the_user_orders.items(), key=lambda x: x[0], reverse=True)
    for i in sort_user_orders:
        displayed_orders[i[0]] = i[1]
    print("Retrieving orders")
    print(test)
    return render_template('trackorders.html', displayed_orders=displayed_orders)

@app.route('/trackordersOldest')
def trackordersoldest():
    # user's order database should be retrieved here - W
    username = ""
    if 'username' in session:
        username = session['username']
    displayed_orders = {} #to be used for display in track orders page
    test = main.order_management.retrieve_all_order_id()
    the_user_orders = {} # This will contain the individual user's orders.
    the_user_order_count = 1 # Store each order with the count as key for sorting.
    for i in test:
        eachorder = main.order_management.retrieve_order_by_id(i)
        print("Object {}".format(eachorder))
        if eachorder.get_username() == username:
            the_user_orders[the_user_order_count] = eachorder
            the_user_order_count += 1
        else:
            pass
    sort_user_orders = sorted(the_user_orders.items(), key=lambda x: x[0])
    for i in sort_user_orders:
        displayed_orders[i[0]] = i[1]
    print("Retrieving orders")
    print(test)
    return render_template('trackordersOldest.html', displayed_orders=displayed_orders)


@app.route('/orderlog/<orderid>')
def orderlog(orderid):
    username = ""
    if 'username' in session:
        username = session['username']
    current_order = {}
    test = main.order_management.retrieve_all_order_id()
    print("The order id is a{}a".format(orderid))
    for i in test:
        print("i is a{}a".format(i))
        if str(i) == str(orderid):
            current_order["Current_Order"] = main.order_management.retrieve_order_by_id(i)
        else:
            print("Order-id not found")
    c = current_order["Current_Order"] # c = order-object!
    print("Status is,", c.get_status())
    if c.get_status() == 0:
        orderstage = "Processing"
    elif c.get_status() == 1:
        orderstage = "Shipped"
    elif c.get_status() == 2:
        orderstage = "Delivered"
    else:
        orderstage = "PaymentPending"
    return render_template('orderlog.html', orderid=orderid, current_order=c, orderstage=orderstage, orderlogCommentDict=c.get_order_log())
    # return render_template('orderlog.html', order_info=order_info, orderlogCommentDict = order_info["orderlogComment"], productname = "processing")


@app.route('/orderlist/<orderid>')
def orderlist(orderid):
    test = main.db.return_object("Order")  # Retrieve all orders dictionary
    current_order = {}
    for i in test["allorders"]:  # Loop thru the orders list to find the correct order, i = orderobject
        if i.get_orderID == orderid:
            current_order["Current_Order"] = i  # creates dictionary with orderid-orderobject pair
        else:
            pass
    c = current_order["Current_Order"]
    return render_template('orderlist.html', current_order=c)


@app.route('/deliverymanagementsystem')
def deliverymanagementsystem():
    return render_template("deliverymanagementsystem.html")


@app.route('/adminorderhistory')
def adminorderhistory():
    displayed_orders = {}
    test = main.db.return_object("Order")  # Retrieve all orders dictionary
    orders_list = test["allorders"]
    all_orders = {}
    all_orders_count = {}
    for eachorder in orders_list:
        all_orders[all_orders_count] = eachorder
        all_orders_count += 1
    else:
        pass  # Skip if order don't belong to user
    sort_user_orders = sorted(all_orders.items(), key=lambda x: x[0])  # Sort based on order-count
    for i in sort_user_orders:
        displayed_orders[i[0]] = i[1]
    return render_template('adminorderhistory.html', display_orders=displayed_orders)


@app.route('/scheduleddeliveries')
def scheduleddeliveries():
    return render_template('scheduleddeliveries.html')


# matt
@app.route('/aboutus')
def aboutus():
    return render_template('AboutUs.html')

# matt
@app.route('/warrenty')
def warrenty():
    return render_template('Warrenty.html')

# matt
@app.route('/aboutus2')
def aboutus2():
    return render_template('AboutUs.html')

# matt
@app.route('/faq2')
def faq1():
    return render_template('FAQ.html')

if __name__ == '__main__':
    app.run()
