from StorageManagement import StorageManagement

# HF
class UserManagement:

    def __init__(self, storage_management):
        self.__key_name = "Users"
        self.__handler = storage_management
        self.__db = None
        print("\n[START OF USERMANAGEMENT INIT]")
        if self.__handler.storage_exist(self.__key_name):
            print("Storage: {} Found, no error".format(self.__key_name))

        else:
            print("Storage: {} not found, creating one".format(self.__key_name))
            self.__handler.create_new_storage(self.__key_name)

        self.__db = self.__handler.get_storage(self.__key_name)
        print("[END OF USERMANAGEMENT INIT]\n")

    def add_user(self, user):
        key_list = list(self.__db.keys())

        if user.get_username() in key_list:
            print("Error, exiting username found, no duplicate allowed")

        else:
            self.__db[user.get_username()] = user
            self.__handler.set_storage(self.__key_name, self.__db)
            print("adding new user: {}".format(user.get_username()))

    def delete_user(self, username):
        key_list = list(self.__db.keys())

        if username in key_list:
            print("deleting user: {}".format(username))
            del self.__db[username]
            self.__handler.set_storage(self.__key_name, self.__db)

        else:
            print("No username found, unable to delete")

    def modify_user(self, user):
        key_list = list(self.__db.keys())

        if user.get_username() in key_list:
            print("modifying user: {}".format(user.get_username()))
            self.__db[user.get_username()] = user
            self.__handler.set_storage(self.__key_name, self.__db)

        else:

            print("No username found, unable to modify")

    def get_user(self, username):
        key_list = list(self.__db.keys())

        if username in key_list:
            print("Getting user: {}".format(username))
            return self.__db[username]

        else:

            print("No username found, unable to get one")
            return None
    
    def get_username_list(self):

        key_list = list(self.__db.keys())

        if key_list == []:

            return None
        else:
            return key_list


