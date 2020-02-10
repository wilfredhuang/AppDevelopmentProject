from wtforms import *
from wtforms.validators import EqualTo, ValidationError

import PasswordHashing
import requests
import main

password_holder = None


class CreateUserForm(Form):
    firstName = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    lastName = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    membership = RadioField('Membership', choices=[('F', 'Fellow'), ('S', 'Senior'), ('P', 'Professional')],
                            default='F')
    gender = SelectField('Gender', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    remarks = TextAreaField('Remarks', [validators.Optional()])


# Validation
# HF
def username_duplication_check(form, field):
    temp = main.db.return_keys("Users")
    temp2 = None
    temp2 = main.db.get_storage("TEMP")
    print("USERNAMEEEE")
    print(temp2)

    # if username found in storage
    if temp != None and (field.data).lower() in temp:

        # if username is not the same as the currently one
        if temp2 != None:
            temp_keys = temp2.keys()
            logged_in_username = None
            if "username" in temp_keys:
                logged_in_username = temp2['username']

            if logged_in_username != None:
                if temp2 != None and (field.data).lower() != logged_in_username:
                    raise ValidationError('Username have been used')

    elif (field.data).lower() == "admin":

        raise ValidationError('Username have been used')


# HF
def username_login_check(form, field):
    global password_holder
    password_holder = None
    temp = main.db.get_storage("Users")
    keys = temp.keys()
    admin_acc = main.db.get_storage("ADMIN")

    if temp != None and (field.data).lower() in keys:
        password_holder = temp[(field.data).lower()].get_password()

    elif admin_acc.get_username() == (field.data).lower():
        password_holder = admin_acc.get_password()

    else:
        raise ValidationError('Username not found')


# HF
def password_login_check(form, field):
    if password_holder != None:
        if not PasswordHashing.verify_password(password_holder, field.data):
            # print("correct pass is {}".format(password_holder))
            raise ValidationError('Password incorrect')
    else:
        raise ValidationError('Password incorrect')


# HF
class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired(), username_login_check])
    password = PasswordField('Password', [validators.DataRequired(), password_login_check])


# HF
class SignUpForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    username = StringField('Username',
                           [validators.Length(min=6, max=15), username_duplication_check, validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=6, max=15), validators.DataRequired(),
                                          EqualTo('confirm_pass', message='Passwords must match')])
    confirm_pass = PasswordField('Confirm Password', [validators.DataRequired()])
    postal_code = StringField('Postal Code', [validators.DataRequired()])
    address = StringField('Street Address', [validators.DataRequired()])
    country = StringField('Country', [validators.DataRequired()])
    city = StringField('City', [validators.DataRequired()])
    unit_number = StringField('Unit Number', [validators.DataRequired()])


# HF
class UserDetailsForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])


# HF
class ChangePasswordForm(Form):
    password = PasswordField('Password', [validators.Length(min=6, max=15), validators.DataRequired(),
                                          EqualTo('confirm_pass', message='Passwords must match')])
    confirm_pass = PasswordField('Confirm Password', [validators.DataRequired()])


# HF
class AddressForm(Form):
    postal_code = StringField('Postal Code', [validators.DataRequired()])
    address = StringField('Street Address', [validators.DataRequired()])
    country = StringField('Country', [validators.DataRequired()])
    city = StringField('City', [validators.DataRequired()])
    unit_number = StringField('Unit Number', [validators.DataRequired()])


# HF
class SalesForm(Form):
    filter_list = ["year", "month", "day", "all"]
    year_list = []
    month_list = []
    day_list = []

    for i in range(1, 32):
        day_list.append((i, i))

    for i in range(1, 13):
        month_list.append((i, i))

    for i in range(2015, 2024):
        year_list.append((i, i))

    filter = SelectField("filter", choices=filter_list)
    year = SelectField("year", choices=year_list)
    month = SelectField("month", choices=month_list)
    day = SelectField("day", choices=day_list)


class CheckoutForm(Form):
    country_list = []
    url = "https://restcountries.eu/rest/v2/all?fields=name;alpha2Code"
    countries = requests.get(url)
    for i in countries.json():
        country_list.append((i['alpha2Code'], i['name']))
    email_address = StringField("Email Address", [validators.DataRequired()])
    full_name = StringField("Full Name", [validators.DataRequired()])
    address = StringField("Shipping Address", [validators.DataRequired()])
    postal_code = StringField('Postal Code', [validators.DataRequired()])
    city = StringField('City', [validators.DataRequired()])
    countries = SelectField("Country", choices=country_list)
    
    
class CreateItemForm(Form):
    item_id = StringField('Item ID: ', [validators.Length(min=1,
                                                          max=150), validators.DataRequired()])
    item_name = StringField('Item Name: ', [validators.Length(min=1,
                                                              max=150), validators.DataRequired()])
    item_cost = FloatField('Item Price: ',[validators.DataRequired()])
    item_quantity = IntegerField('Item Quantity:', [validators.NumberRange(min=0, max=1000), validators.DataRequired()])
    item_type = RadioField('Item Type: ', choices=[('W', 'Wired'),
                                                   ('WL', 'Wireless')], default='W', )
    remarks = TextAreaField('Remark', [validators.Optional()])


class SearchForm(Form):
    search = StringField('Search: ')

