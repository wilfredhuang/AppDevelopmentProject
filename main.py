"""
    This file will deal with overall of the project
    Most classes will be linked to this file
    This is to manage all different class to make it organised
    Note: Do not modify this before asking me (HF)
"""
from StorageManager import StorageManager
from UserManagement import UserManagement
from SessionManagement import SessionManagement
from StorageHandler import StorageHandler
import PasswordHashing
from Admin import Admin
db = None
user_management = None
session_management = None
storage_management = None
storage_handler = None

# HF
def init():

    global db
    global user_management
    global session_management
    global storage_handler

    storage_handler = StorageHandler()
    db = StorageManager()
    user_management = UserManagement(storage_handler)
    session_management = SessionManagement(storage_handler)
    #print("Main testing")
    #storage_management.storage_exist('Users')

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