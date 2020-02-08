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
# from SessionManagement import SessionManagement

db = None

# session_management = None
user_management = None
storage_management = None
storage_handler = None
cart_management = None

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

    storage_handler = StorageHandler()
    db = StorageManager()
    user_management = UserManagement(storage_handler)
    cart_management = CartManagement(storage_handler)
    # session_management = SessionManagement(storage_handler)

# DO NOT TOUCH, UNLESS ASKED
def reset():
    pass
    #StorageManager.reset()


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