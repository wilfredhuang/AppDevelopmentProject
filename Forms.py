from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, PasswordField
from wtforms.validators import EqualTo, Email, ValidationError
import main
import PasswordHashing

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

        #if username is not the same as the currently one
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

def password_login_check(form, field):
    if password_holder != None:
        if not PasswordHashing.verify_password(password_holder, field.data):

            #print("correct pass is {}".format(password_holder))
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
    username = StringField('Username', [validators.Length(min=6, max=15), username_duplication_check, validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=6, max=15), validators.DataRequired(), EqualTo('confirm_pass', message='Passwords must match')])
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