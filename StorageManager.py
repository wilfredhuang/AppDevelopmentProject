# Please read the instruction before using
# This will control all persistent storage (eg. Add, Delete, Modify)
# Note: Do not modify this before asking me (HF)
# HF

import shelve

class StorageManager():

    def __init__(self):
        # error checking
        try:
            self.__db = shelve.open('storage.db', 'r')
            self.__db.close()
        except Exception:
            print("Storage not found")

        self.delete_storage('TEMP')

    def is_key_found(self, name):

        keys = self.__db.keys()
        if name in keys:
            return True
        else:
            return False


    def reset(self):
        self.__db = shelve.open('storage.db', 'c')
        keys = list(self.__db.keys())

        for p in keys:
            del self.__db[p]
        self.__db.close()

    def create_new_storage(self, name, items=None, dict=True):
        self.__db = shelve.open('storage.db', 'c')
        # items must be a dictionary or list
        if(self.is_key_found(name) == False):

            if items == None:

                if dict == True:
                    self.__db[name] = {}
                    print("Created dictionary")
                elif dict == False:
                    self.__db[name] = []
                    print("Created list")
            else:
                self.__db[name] = items
                print("Created storage")
        else:
            print("existing name of storage found")
        self.__db.close()

    def delete_storage(self, name):
        self.__db = shelve.open('storage.db', 'c')
        if(self.is_key_found(name) == True):
            del self.__db[name]
            print("Deleted storage")
        else:
            print("no keys found with the given name")
        self.__db.close()

    def set_storage(self, name, item):
        self.__db = shelve.open('storage.db', 'c')
        if(self.is_key_found(name) == True):
            self.__db[name] = item
            print("modified storage")

        else:
            print("Unable to set item due to storage name not found")
        self.__db.close()

    def add_item(self, storage_name, key_to_use, item):
        self.__db = shelve.open('storage.db', 'c')
        if(self.is_key_found(storage_name) == True):
            print("storage name found")

            print(self.__db[storage_name])

            if key_to_use in self.__db[storage_name].keys():
                print("Key is in used")
                print("ALL USERS: ")
                print(self.__db[storage_name].keys())

            else:
                temp = self.__db[storage_name]
                print("Key is not in used")
                temp[key_to_use] = item
                self.__db[storage_name] = temp
                print("ALL USERS: ")
                print(self.__db[storage_name].keys())


        else:
            print("Unable to set item due to storage name not found")

        self.__db.close()

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