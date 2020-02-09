"""
HF
All Management will inherit from this class
Management will have basics stuffs of adding, deleting, modifying and retrieving stuffs

db is a storage only for this class and when changes are made, storage handle will be
called to update the shelf(Persistent storage)

"""


class ManagementSystem:  # get storage

    def __init__(self, key_name, name, storage_handler):
        self._key_name = key_name
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

    def print_keys(self):
        key_list = list(self._db.keys())

        print("PRINTING KEYS FOR {}".format(self._key_name))
        print(key_list)

