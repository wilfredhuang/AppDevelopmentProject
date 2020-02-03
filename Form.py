from wtforms import Form, StringField, RadioField, TextAreaField, validators


class CreateItemForm(Form):
    item_id = StringField('Item ID: ', [validators.Length(min=1,
                                                          max=150), validators.DataRequired()])
    item_name = StringField('Item Name: ', [validators.Length(min=1,
                                                              max=150), validators.DataRequired()])
    item_cost = StringField('Item Price: ', [validators.Length(min=1,
                                                               max=150), validators.DataRequired()])
    item_quantity = StringField('Item Quantity:', [validators.Length(min=1,
                                                                     max=150), validators.DataRequired()])
    item_type = RadioField('Item Type: ', choices=[('W', 'Wired'),
                                                   ('WL', 'Wireless')], default='W', )
    remarks = TextAreaField('Remark', [validators.Optional()])


class SearchForm(Form):
    search = StringField('Search: ')
