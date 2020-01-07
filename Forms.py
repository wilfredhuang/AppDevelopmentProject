from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, PasswordField
from wtforms.validators import EqualTo, Email


class CreateUserForm(Form):
    firstName = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    lastName = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    membership = RadioField('Membership', choices=[('F', 'Fellow'), ('S', 'Senior'), ('P', 'Professional')],
                            default='F')
    gender = SelectField('Gender', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    remarks = TextAreaField('Remarks', [validators.Optional()])


# HF
class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])


# HF
class SignUpForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    username = StringField('Username', [validators.Length(min=6, max=15), validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired(), Email(message=None), EqualTo('CEmail', message='Email must match')])
    confirm_email = StringField('Re-enter Email', [validators.DataRequired(), Email(message=None)])
    password = PasswordField('Password', [validators.Length(min=6, max=15), validators.DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm_pass = PasswordField('Confirm Password', [validators.DataRequired()])
    postal_code = StringField('Postal Code', [validators.DataRequired()])
    address = StringField('Street Address', [validators.DataRequired()])
    country = StringField('Country', [validators.DataRequired()])
    city = StringField('City', [validators.DataRequired()])
    unit_number = StringField('Unit Number', [validators.DataRequired()])

