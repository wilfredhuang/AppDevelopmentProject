from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session

from Forms import *
from binascii import hexlify
import User, main, Product, os, paypalrestsdk, requests, Order
import PasswordHashing
import shelve
import uuid
import Item
import storageManagerFunction_Hieu
from Form import *
import pandas as pd

UPLOAD_FOLDER = 'static/files'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
SECRET_KEY = os.urandom(24)
app.secret_key = SECRET_KEY
main.init()
storageManagerFunction_Hieu.init()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#H
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#H
def retrieveFiles():
    entries = os.listdir(app.config['UPLOAD_FOLDER'])
    fileList = []
    for entry in entries:
        fileList.append(entry)
    return fileList

#H
def get_inventory():
    inventory = storageManagerFunction_Hieu.db.get_storage("Inventory")
    return inventory

#H
def get_sale():
    sale = storageManagerFunction_Hieu.db.get_storage("Inventory")
    return sale

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

# HF
@app.route("/SignOut")
def SignOut():
    del session['username']
    login_form = LoginForm(request.form)
    return redirect(url_for('loginMenu'))


# Figuring out carting system
# JH
# STILL TESTING
@app.route("/testAddItem", methods=["GET", "POST"])
def testAddItem():
    # HOW TO USE ORDERS 101
    test = main.db.return_object("Order")  # This returns the entire Order database
    test = test["allorders"]  # This returns the entire Order database
    for i in test:  # If you want to filter specific usernames for your part just use if i.get_username == "username"
        print(f"Item name: {i.get_item_list()[0].get_name()}, Total Price: {i.get_productPrice()}, "
              f"Address: {i.get_address()}, Status: {i.get_status()}, Username: {i.get_username()}")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer A21AAGQd_-Ms2SOo-n_eZq-f9pfeoYQEdPOdxCUnZhvO_cWpOMckpKaqGWeKNSDpWiDuYbLdMI8U2YZ7gbuYKYM36S2fa4kMA'
    }
    response = requests.get("https://api.sandbox.paypal.com/v1/identity/oauth2/userinfo?schema=paypalv1.1", headers=headers)
    print(response.json())
    username = ""
    if 'username' in session:
        username = session['username']
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
            #main.db.update_cart("Cart", "TestUser", productList)
            main.db.update_cart("Cart", username, productList)
            print("-- TEST --")
            test = main.db.return_object("Cart")
            #test = test["TestUser"]
            test = test[username]
            # print(f"Product Name: {test.get_name()}, Cost: {test.get_cost()}, ID: {test.get_id()}")
            print(test[0].get_name())
            print(test[1].get_name())
            print("-- TEST --")
        elif request.form["submit_button"] == "Delete":
            print("Delete item button pressed")
            main.db.get_storage("Cart", True, True)
            main.db.delete_storage("Cart")
    return redirect(url_for('productDisplay'))


# Shopping cart page
# JH
# STILL TESTING
@app.route("/cart", methods=["GET", "POST"])
def cart():
    total_cost = 0
    username = ""
    if 'username' in session:
        username = session['username']
    if request.method == "POST":
        try:
            item = main.db.return_object("Cart")
            item = item[username]
            #item = item["TestUser"]
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
                        #main.db.add_item("Cart", "TestUser", item)
                        main.db.add_item("Cart", username, item)
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
                        #main.db.add_item("Cart", "TestUser", item)
                        main.db.add_item("Cart", username, item)
                print("---TEST---")
            # Get total cost
            for i in item:
                total_cost += float(i.get_cost()) * float(i.get_quantity())
        except:
            pass



    main.db.get_storage("Cart", True, True)
    product_object = main.db.return_object("Cart")
    try:
        product_object = product_object[username]
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
    form = CheckoutForm(request.form)
    if request.method == "POST" and form.validate():
        data = []
        data.append(form.address.data)
        data.append(form.countries.data)
        main.db.get_storage("temp_paypal", True, True)
        main.db.update_cart("temp_paypal", "paypal", data)
        return redirect(url_for('payment'))
    return render_template("g_checkout.html", form=form)

# Logged In Checkout - TESTING ONLY, NOT FINAL!!!!!
# JH
@app.route("/usercheckout", methods=["GET", "POST"])
def user_checkout():
    main.db.get_storage("Users", True, True)
    user = main.db.return_object("Users")
    user = user["tristan"]
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
    username = ""
    if 'username' in session:
        username = session['username']
    data = main.db.return_object("temp_paypal")
    data = data["paypal"]  # 0: address, 1:country code
    # ----------
    item_list = []
    total_cost = 0
    # Get cart
    item = main.db.return_object("Cart")
    item = item[username]
    for i in item:
        item_list.append({"name": i.get_name(),
                          "sku": "1",
                          "price": i.get_cost(),
                          "currency": "SGD",
                          "quantity": "1"})
        total_cost += float(i.get_cost()) * float(i.get_quantity())
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

    new_order = Order.Order(item, total_cost, data[0], "0", username)
    order_list.append(new_order)
    main.db.update_cart("Order", "allorders", order_list)
    print("-----HELLO BODOH-------")
    print(order_list)
    print(new_order)
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
    success = False
    payment = paypalrestsdk.Payment.find(request.form["paymentID"])
    if payment.execute({"payer_id": request.form["payerID"]}):
        print("Execute Sucess!")
        print(payment.amount)
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
        return render_template("aboutUs.html")

    if request.method=='GET':
        try:
            feedback=main.db.return_object('feedback')
            feedback=feedback['testfeedback']
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



#Hieu
@app.route('/adminItemDashboard', methods=['Get', 'Post'])
def adminItemDashboard():
    search_function = SearchForm(request.form)
    key = ""
    if request.method == 'POST':
        key = search_function.search.data
    print(f'key is {key}')

    return render_template('adminItemDashboard.html', ItemList=get_inventory().values(), input=search_function,
                           key_search=key, alarm_stock=10)

#Hieu
@app.route('/createItem', methods=['Get', 'Post'])
def addItem():
    createItemForm = CreateItemForm(request.form)
    if request.method == 'POST':

        filename = str(uuid.uuid4()) + createItemForm.item_id.data + '.jpg'

        if createItemForm.item_type.data == "W":
            item = Item.Wired(createItemForm.item_id.data, createItemForm.item_name.data, createItemForm.item_cost.data,
                              filename)
        elif createItemForm.item_type.data == "WL":
            item = Item.Wireless(createItemForm.item_id.data, createItemForm.item_name.data,
                                 createItemForm.item_cost.data, filename)

        item.set_stock(createItemForm.item_quantity.data)
        storageManagerFunction_Hieu.db.get_storage("Inventory", True, True)
        storageManagerFunction_Hieu.db.add_item("Inventory", item.get_id(), item)

        print(request.files)
        print(request.files['file'])
        print(filename)

        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return redirect(url_for('adminItemDashboard'))
    return render_template('adminCreateItem.html', form=createItemForm)

#Hieu
@app.route('/addItemExcel', methods=['GET', 'POST'])
def addItemExcel():
    db = shelve.open('storage.db', 'w')
    inventory = get_inventory()
    item = ''

    if request.method == 'POST':
        file = request.files['file']
        data = pd.read_excel(file)  # read the file

        for i in range(len(data.index.values)):
            id = data['ID'][i]
            name = data['Name'][i]
            cost = data['Cost'][i]
            stock = data['Stock'][i]
            image = 'none'
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

                inventory[item.get_id()] = existing_item
                db['Inventory'] = inventory

            else:
                item.set_stock(stock)
                storageManagerFunction_Hieu.db.add_item("Inventory", item.get_id(), item)
        db.close()
        return redirect(url_for('adminItemDashboard'))
    return render_template('admin_CreateItem_Excel.html')

#Hieu
@app.route('/removeItem/<id>', methods=['POST'])
def removeItem(id):
    db = shelve.open('storage.db', 'w')
    itemInventory = db['Inventory']
    print(id)
    print(itemInventory)
    removedItem = itemInventory[id]
    try:
        os.remove(f'files/{removedItem.get_file()}')
    except:
        print('error. file not found')
        

    itemInventory.pop(id)
    print('Item removed.')
    print(itemInventory)

    db['Inventory'] = itemInventory
    db.close()

    return redirect(url_for('adminItemDashboard'))

#Hieu
@app.route('/updateItem/<id>', methods=['GET', 'POST'])
def updateItem(id):
    updateItemForm = CreateItemForm(request.form)
    if request.method == 'POST' and updateItemForm.validate():
        db = shelve.open('storage.db', 'w')
        itemInventory = db['Inventory']

        item = itemInventory.get(id)

        item.set_id(updateItemForm.item_id.data)
        item.set_name(updateItemForm.item_name.data)
        item.set_cost(updateItemForm.item_cost.data)
        item.set_stock(updateItemForm.item_quantity.data)

        db['Inventory'] = itemInventory
        db.close()

        return redirect(url_for('adminItemDashboard'))

    else:
        db = shelve.open('storage.db', 'w')
        itemInventory = db['Inventory']
        db.close()

        item = itemInventory.get(id)
        updateItemForm.item_id.data = item.get_id()
        updateItemForm.item_name.data = item.get_name()
        updateItemForm.item_quantity.data = item.get_stock()
        updateItemForm.item_cost.data = item.get_cost()
        updateItemForm.item_type.data = item.get_type()

        return render_template('adminUpdateItem.html', form=updateItemForm)


@app.route('/productDisplay')
def productDisplay():
    ItemList = []
    if get_inventory() is not None:
        ItemList = get_inventory().values()
    else:
        pass

    return render_template('productDisplay.html', ItemList=ItemList)

# Wilfred's delivery section

@app.route('/trackorders/')
def trackorders():
    # user's order database should be retrieved here - W
    displayed_orders = {} #to be used for display in track orders page
    test = main.db.return_object("Order")
    orders_list = test["allorders"] # creates a list with all order instances as each element.
    the_user_orders = {} # This will contain the individual user's orders.
    the_user_order_count = 1 # Store each order with the count as key for sorting.
    for eachorder in orders_list: # loop through database with all orders
        if eachorder.get_username() == "username": # check and add whichever orders that belong to user to his own user orders dictionary
            the_user_orders[the_user_order_count] = eachorder
            the_user_order_count += 1
        else:
            pass # Skip if order don't belong to user
    sort_user_orders = sorted(the_user_orders.items(), key=lambda x: x[0], reverse=True)  # Sort based on order-id
    for i in sort_user_orders:
        displayed_orders[the_user_orders[i].get_orderID()] = the_user_orders[i].get_order_date() #store each item as orderid-order_date pair
    return render_template('trackorders.html', displayed_orders=displayed_orders)


@app.route('/trackordersOldest')
def trackordersoldest():
    # user's order database should be retrieved here - W
    displayed_orders = {} #to be used for display in track orders page
    test = main.db.return_object("Order")
    orders_list = test["allorders"] # creates a list with all order instances as each element.
    the_user_orders = {} # This will contain the individual user's orders.
    the_user_order_count = 1 # Store each order with the count as key for sorting.
    for eachorder in orders_list: # loop through database with all orders
        if eachorder.get_username() == "username": # check and add whichever orders that belong to user to his own user orders dictionary
            the_user_orders[the_user_order_count] = eachorder
            the_user_order_count += 1
        else:
            pass # Skip if order don't belong to user
    sort_user_orders = sorted(the_user_orders.items(), key=lambda x: x[0])  # Sort based on order-id
    for i in sort_user_orders:
        displayed_orders[the_user_orders[i].get_orderID()] = the_user_orders[i].get_order_date() #store each item as orderid-order_date pair
    return render_template('trackorders.html', displayed_orders=displayed_orders)

if __name__ == '__main__':
    app.run()
