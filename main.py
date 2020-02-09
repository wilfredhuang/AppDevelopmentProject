"""
HF

This file will deal with overall of the project
Most classes will be linked to this file
This is to manage all different class to make it organised



"""
from StorageManager import StorageManager
from UserManagement import UserManagement
from StorageHandler import StorageHandler
from CartManagement import CartManagement
from OrderManagement import OrderManagement
from c_SalesManagement import SalesManagement
from ProductManagement import ProductManagement
from ProductManagement import ProductManagement
from c_SalesManagement import SalesManagement
from ProductManagement import *
from oauth2client.service_account import ServiceAccountCredentials
# from SessionManagement import SessionManagement

db = None

# session_management = None
user_management = None
storage_management = None
storage_handler = None
cart_management = None
order_management = None
product_management = None
sales_management = None
"""
Init is needed to setup the project when started
All storage need to be created / retrieved before use
"""


# HF
def init():

    global db

    # global session_management
    global user_management
    global storage_handler
    global cart_management
    global order_management
    global product_management
    global sales_management
    global product_management

    storage_handler = StorageHandler()
    db = StorageManager()
    
    user_management = UserManagement(storage_handler)
    cart_management = CartManagement(storage_handler)
    product_management = ProductManagement(storage_handler)
    sales_management = SalesManagement(storage_handler)
    order_management = OrderManagement(storage_handler, sales_management)
    # session_management = SessionManagement(storage_handler)


# DO NOT TOUCH, UNLESS ASKED
def reset():
    pass
    #StorageManager.reset()

# The scope for the OAuth2 request.
SCOPE = 'https://www.googleapis.com/auth/analytics.readonly'

# The location of the key file with the key data.
KEY_FILEPATH = 'mimetic-heaven-267214-a894f52e042d.json'

# Defines a method to get an access token from the ServiceAccount object.
def get_access_token():
  return ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILEPATH, SCOPE).get_access_token().access_token

def test_mode():
    """
    storage = SM.StorageManager()
    storage.create_new_storage("testing", [1, 2, 3])
    #storage.delete_storage("testing")
    #print(storage.return_keys())
    print("hi")
    temp = storage.get_storage("testing")
    temp = [1, 2]
    storage.set_storage("testing",[1,2])
    print("TEMP:")
    print(temp)
    print("DB:")
    print(storage.get_storage("testing"))
    """
    #init()

    #print("This is main func")
    #storage_management.testprint()
    """
    new_pass = PasswordHashing.hash_password("appdev")

    new_acc = Admin("admin", new_pass)
    db.set_storage("ADMIN", new_acc)

    temp = db.get_storage("ADMIN")
    print("does pass match")
    print(PasswordHashing.verify_password(temp.get_password(), "appdev"))
    """
#test_mode()


# H
def get_inventory():
    inventory = storage_handler.get_storage('Product')
    if inventory is not None:
        return inventory
    else:
        inventory = {}
        return inventory
