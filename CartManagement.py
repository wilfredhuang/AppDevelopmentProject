"""
JH
w0t
"""

from ManagementSystem import ManagementSystem


class CartManagement(ManagementSystem):

    def __init__(self, storage_handler):
        super().__init__("Cart", "Cart Management", storage_handler)

    def add_to_cart(self, username, item):
        item_list = self.retrieve_cart(username)
        # Check if already existing in cart
        item_exist = False
        for i in item_list:
            if i.get_name() == item.get_name():
                i.add_quantity()
                item_exist = True
                break
        if not item_exist:
            item_list.append(item)
        key_list = list(self._db.keys())
        self._db[username] = item_list
        self._handler.set_storage(self._key_name, self._db)

    def retrieve_cart(self, username):
        key_list = list(self._db.keys())
        if username in key_list:

            return self._db[username]
        else:
            return []

    def cart_quantity(self, username, item_name, action):
        key_list = list(self._db.keys())
        item_list = self.retrieve_cart(username)
        for i in item_list:
            if i.get_name() == item_name:
                if action == "add":
                    i.add_quantity()
                elif action == "remove":
                    if i.get_quantity() >= 2:
                        i.remove_quantity()
                    else:
                        x = item_list.index(i)
                        item_list.pop(x)
                break
        self._db[username] = item_list
        self._handler.set_storage(self._key_name, self._db)

    def clear_cart_debug(self, username):
        key_list = list(self._db.keys())
        if username in key_list:
            self._db[username] = []
            self._handler.set_storage(self._key_name, self._db)
    # def delete_user(self, username):
    #     key_list = list(self._db.keys())
    #
    #     if username in key_list:
    #         print("deleting user: {}".format(username))
    #         del self._db[username]
    #         self._handler.set_storage(self._key_name, self._db)
    #
    #     else:
    #         print("No username found, unable to delete")
    #
    # def modify_user(self, user):
    #     key_list = list(self._db.keys())
    #
    #     if user.get_username() in key_list:
    #         print("modifying user: {}".format(user.get_username()))
    #         self._db[user.get_username()] = user
    #         self._handler.set_storage(self._key_name, self._db)
    #
    #     else:
    #
    #         print("No username found, unable to modify")
    #
    # def get_user(self, username):
    #     key_list = list(self._db.keys())
    #
    #     if username in key_list:
    #         print("Getting user: {}".format(username))
    #         return self._db[username]
    #
    #     else:
    #
    #         print("No username found, unable to get one")
    #         return None
    #
    # def get_username_list(self):
    #
    #     key_list = list(self._db.keys())
    #
    #     if key_list == []:
    #
    #         return None
    #
    #     else:
    #         return key_list
    #
    #
