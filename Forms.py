from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, PasswordField

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


class SignUpForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    email = StringField('Username', [validators.DataRequired()])
    confirm_pass = PasswordField('CPassword', [validators.DataRequired()])
    postal_code = StringField('Username', [validators.DataRequired()])
    address = StringField('Address', [validators.DataRequired()])


