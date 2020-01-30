from StorageHandler import StorageHandler

# HF
class SessionManagement:

    def __init__(self, StorageHandler):
        self.__key_name = "TEMP"
        self.__handler = StorageHandler
        self.__db = None
        print("\n[START OF SESSION INIT]")
        if self.__handler.storage_exist(self.__key_name):
            print("Storage: {} Found, no error".format(self.__key_name))
            self.__handler.delete_storage(self.__key_name)

            print("Storage: {} resetting, creating new one".format(self.__key_name))
            self.__handler.create_new_storage(self.__key_name)
        else:
            print("Storage: {} not found, creating one".format(self.__key_name))
            self.__handler.create_new_storage(self.__key_name)

        self.__db = self.__handler.get_storage(self.__key_name)
        print("[END OF SESSION INIT]\n")

    def add_item(self, key, item):

        key_list = list(self.__db.keys())

        if key in key_list:
            print("storage: Error, exiting key found, no duplicate allowed")

        else:
            self.__db[key] = item
            self.__handler.set_storage(self.__key_name, self.__db)
            print("adding new item: {}".format(key))

    def delete_item(self):
        pass

    def modify_item(self):
        pass

    def get_keys(self):
        key_list = list(self.__db.keys())
        if key_list == []:

            return None
        else:
            return key_list

