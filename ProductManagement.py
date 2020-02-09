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
            print("adding new item: {}, {} units".format(item.get_id(),item.get_quantity()))

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