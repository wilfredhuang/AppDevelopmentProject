from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, PasswordField
from wtforms.validators import EqualTo, Email, ValidationError
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
    if temp != None and (field.data).lower() in temp:

        raise ValidationError('Username have been used')

def username_login_check(form, field):
    temp = main.db.get_storage("Users")
    keys = temp.keys()

    if temp != None and (field.data).lower() in keys:

        global password_holder
        password_holder = temp[(field.data).lower()].get_password()

    else:
        raise ValidationError('Username not found')

def password_login_check(form, field):
    if not field.data == password_holder:

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

