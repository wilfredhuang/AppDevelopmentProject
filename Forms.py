from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, PasswordField
from wtforms.validators import EqualTo, Email, ValidationError
import shelve

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
def email_check(form, field):
    if (field.data).lower() == "aaaaaa":
        raise ValidationError('Username have been used')

"""temp_dict = None
try:
    temp_dict = shelve.open('user_storage.db', 'r')
except:
    print("Error in retrieving Users from storage.db.")

if temp_dict != None:
    for email in temp_dict:
        if field.data.lower() != email:
            raise ValidationError('Username have not been used')"""


def username_check(form, field):
    temp_dict = None
    """
    try:
        temp_dict = shelve.open('user_storage.db', 'r')

    except IndexError:
        print("Error in retrieving Users from storage.db")
    """
    if temp_dict != None:
        for email in temp_dict:
            if field.data.lower() != email:
                raise ValidationError('Username have not been used')



# HF
class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])


# HF
class SignUpForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    username = StringField('Username', [validators.Length(min=6, max=15), username_check, validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=6, max=15), validators.DataRequired(), EqualTo('confirm_pass', message='Passwords must match')])
    confirm_pass = PasswordField('Confirm Password', [validators.DataRequired()])
    postal_code = StringField('Postal Code', [validators.DataRequired()])
    address = StringField('Street Address', [validators.DataRequired()])
    country = StringField('Country', [validators.DataRequired()])
    city = StringField('City', [validators.DataRequired()])
    unit_number = StringField('Unit Number', [validators.DataRequired()])

