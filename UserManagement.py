from StorageManagement import StorageManagement

class UserManagement():

    def __init__(self):
        self.__key_name = "Users"
        self.__handler = StorageManagement()
        self.__db = None

        if self.__handler.storage_exist(self.__key_name):
            pass

        else:
            self.__handler.create_new_storage(self.__key_name)

    def add_user(self):
        pass

    def delete_user(self):
        pass

    def modify_user(self):
        pass

    def get_user(self):
        pass
    
    def get_username_list(self):
        pass


