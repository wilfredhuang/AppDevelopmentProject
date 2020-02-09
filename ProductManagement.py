"""
management of products etc
1. add new item
2. update existing item stocks & etc
3. delete existing item - if low sale, no longer in production, etc
4. display Item on the web page for user interactivity
"""

from ManagementSystem import ManagementSystem


class ProductManagement(ManagementSystem):

    def __init__(self, storage_handler):
        super().__init__("Product", "Product Management", storage_handler)

    def update_item(self, item):
        key_list = list(self._db.keys())

        if item.get_id() in key_list:
            temp_item = self._db[item.get_id()]
            temp_item.set_quantity(temp_item.get_quantity() + item.get_quantity())
            self._db[item.get_id()] = temp_item
            self._handler.set_storage(self._key_name, self._db)
            print("existing item: {} found, updating quantity".format(item.get_id()))
            print("Total quantity: {}".format(temp_item.get_quantity()))

        else:
            self._db[item.get_id()] = item
            self._handler.set_storage(self._key_name, self._db)
            print("adding new item: {}, {} units".format(item.get_id(), item.get_quantity()))

            print("adding new item: {}, {} units".format(item.get_id(), item.get_quantity()))

    def purchase_item(self, item_list):
        key_list = list(self._db.keys())

        for item in item_list:
            if item.get_id() in key_list:
                temp_item = self._db[item.get_id()]
                temp_item.set_quantity(temp_item.get_quantity() - item.get_quantity())
                self._db[item.get_id()] = temp_item
                self._handler.set_storage(self._key_name, self._db)
                print("existing item: {} found, purchasing {} item".format(item.get_id(), item.get_quantity()))
                print("Total quantity left: {}".format(temp_item.get_quantity()))

            else:
                print("NO ITEM FOUND, ERROR")

    def delete_item(self, item):
        key_list = list(self._db.keys())

        if item in key_list:
            print(f"deleting item: {item}")
            del self._db[item]
            self._handler.set_storage(self._key_name, self._db)

        else:
            print("No item found, unable to delete")

    def modify_product(self, item):
        key_list = list(self._db.keys())

        if item.get_id() in key_list:
            print("modifying user: {}".format(item.get_id()))
            self._db[item.get_id()] = item
            self._handler.set_storage(self._key_name, self._db)

        else:

            print("No product found, unable to modify")
