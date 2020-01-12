"""
    This file will deal with overall of the project
    Most classes will be linked to this file
    This is to manage all different class to make it organised
    Note: Do not modify this before asking me (HF)
"""
from StorageManager import StorageManager
db = None

# HF
def init():
    global db
    db = StorageManager()

def reset():
    StorageManager.reset()


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
    init()

   # print("KEYTSSSSSSSS")
    #db.delete_storage("Users")
    #db.return_keys()
    #print(db.return_keys("Users"))
    temp = db.get_storage("Users")
    print("TEST")
    print(list(temp.keys()))
test_mode()