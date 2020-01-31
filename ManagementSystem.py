class ManagementSystem:
    def __init__(self, key_name, name, storage_handler):
        self._key_name = "Users"
        self._handler = storage_handler
        self._db = None

        print("\n[START OF '{}' INIT]".format(name))
        if self._handler.storage_exist(self._key_name):
            print("Storage: {} Found, no error".format(self._key_name))

        else:
            print("Storage: {} not found, creating one".format(self._key_name))
            self._handler.create_new_storage(self._key_name)

        self._db = self._handler.get_storage(self._key_name)
        print("[END OF '{}' INIT]\n".format(name))

    def add_item(self):
        pass

    def delete_item(self):
        pass

    def modify_item(self):
        pass


