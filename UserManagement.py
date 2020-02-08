"""
HF
All users related stuffs is being handled here
"""

from ManagementSystem import ManagementSystem



class UserManagement(ManagementSystem):

    def __init__(self, storage_handler):
        #self.__key_name = "Users"
        #self.__handler = storage_handler
        #self.__db = None
        super().__init__("Users", "User Management", storage_handler)

    def add_user(self, user):
        key_list = list(self._db.keys())

        if user.get_username() in key_list:
            print("Error, exiting username found, no duplicate allowed")

        else:
            self._db[user.get_username()] = user
            self._handler.set_storage(self._key_name, self._db)
            print("adding new user: {}".format(user.get_username()))

    def delete_user(self, username):
        key_list = list(self._db.keys())

        if username in key_list:
            print("deleting user: {}".format(username))
            del self._db[username]
            self._handler.set_storage(self._key_name, self._db)

        else:
            print("No username found, unable to delete")

    def modify_user(self, user):
        key_list = list(self._db.keys())

        if user.get_username() in key_list:
            print("modifying user: {}".format(user.get_username()))
            self._db[user.get_username()] = user
            self._handler.set_storage(self._key_name, self._db)

        else:

            print("No username found, unable to modify")

    def get_user(self, username):
        key_list = list(self._db.keys())

        if username in key_list:
            print("Getting user: {}".format(username))
            return self._db[username]

        else:

            print("No username found, unable to get one")
            return None
    
    def get_username_list(self):

        key_list = list(self._db.keys())

        if key_list == []:

            return None

        else:
            return key_list


