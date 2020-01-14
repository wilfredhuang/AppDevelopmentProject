# Please read the instruction before using
# This will control all persistent storage (eg. Add, Delete, Modify)
# Note: Do not modify this before asking me (HF)
# HF

import shelve
""" 
EXPLANATION
* Everything will be stored in "storage.db" shelve
* anything can be stored in database and shelve works like dictionary so we need
* 1. items to be stored at
* 2. the key used to store those items

 
"""
class StorageManager():

    def __init__(self):
        # error checking only
        try:
            self.__db = shelve.open('storage.db', 'r')
            self.__db.close()
        except Exception:
            print("Storage not found")

        # This works like a session storage, things can be stored at 'TEMP' but will be deleted when restart
        self.delete_storage('TEMP')

    # This function can only be use inside this class
    def is_key_found(self, name):

        keys = self.__db.keys()
        if name in keys:
            return True
        else:
            return False

    # Resets storage, delete everything inside db
    # !!!! do not anyhow use
    def reset(self):
        self.__db = shelve.open('storage.db', 'c')
        keys = list(self.__db.keys())

        for p in keys:
            del self.__db[p]
        self.__db.close()

    # create not storage
    def create_new_storage(self, name, items=None, dict=True):
        self.__db = shelve.open('storage.db', 'c')
        # items must be a dictionary or list
        if(self.is_key_found(name) == False):

            # If no item is specified
            if items == None:

                # Default will create a dictionary inside the db with the name parameter as key
                # Unless dict parameter is false which will create list instead
                # eg. db[name] = empty dictionary / list
                if dict == True:
                    self.__db[name] = {}
                    print("Created dictionary")
                elif dict == False:
                    self.__db[name] = []
                    print("Created list")

            # If items are specified
            else:
                self.__db[name] = items
                print("Created storage")
        # if storage with the name parameter is found, will prompt the storage name is in used
        else:
            print("existing name of storage found")
        self.__db.close()

    # delete whole storage with the key as the name

    def delete_storage(self, name):

        self.__db = shelve.open('storage.db', 'c')
        if(self.is_key_found(name) == True):
            del self.__db[name]
            print("Deleted storage")
        else:
            print("no keys found with the given name")
        self.__db.close()

    # Set the whole storage as item with the key as the name
    def set_storage(self, name, item):
        self.__db = shelve.open('storage.db', 'c')
        if(self.is_key_found(name) == True):
            self.__db[name] = item
            print("modified storage")

        else:
            print("Unable to set item due to storage name not found")
        self.__db.close()

    # add a single item after going INTO the storage using the name
    def add_item(self, storage_name, key_to_use, item):
        self.__db = shelve.open('storage.db', 'c')
        if(self.is_key_found(storage_name) == True):
            print("storage name found")

            print(self.__db[storage_name])

            # if item exist inside the storage
            if key_to_use in self.__db[storage_name].keys():
                print("Key is in used")
                print("ALL USERS: ")
                print(self.__db[storage_name].keys())

            # add, if item does not exit
            else:
                temp = self.__db[storage_name]
                print("Key is not in used")
                temp[key_to_use] = item
                self.__db[storage_name] = temp
                print("ALL USERS: ")
                print(self.__db[storage_name].keys())

        # if item storage does not exit
        else:
            print("Unable to set item due to storage name not found")

        self.__db.close()

    # get the whole storage back using the name
    def get_storage(self, name, create=False, dict=False):
        self.__db = shelve.open('storage.db', 'c')

        if (self.is_key_found(name) == True):
            temp = self.__db[name]
            self.__db.close()
            print("Storage found")
            return temp

        else:
            print("storage name not found")
            if create == True:
                print("proceeds to create a new one")
                if dict == True:
                    self.__db[name] = {}
                    print("Created dictionary")
                else:
                    self.__db[name] = []
                    print("Created List")

            self.__db.close()

    # check if storage exist returns true or false
    def check_exist(self, name):
        self.__db = shelve.open('storage.db', 'c')

        if (self.is_key_found(name) == True):
            self.__db.close()
            return True
        else:
            self.__db.close()
            return False


    # TEST USE ONLY

    def return_keys(self, name = None):
        self.__db = shelve.open('storage.db', 'c')
        if(name == None):
            temp = list(self.__db.keys())
            self.__db.close()
            return temp

        elif(name in list(self.__db.keys())):
            temp = list(self.__db[name].keys())
            self.__db.close()
            return temp
        else:
            return None

    # TESTS WROTE BY JH
    def return_object(self, name):
        self.__db = shelve.open('storage.db', 'c')
        temp = self.db
        self.__db.close()

        return temp
    
