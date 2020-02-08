from ManagementSystem import ManagementSystem
from Order import Order
import uuid


class OrderManagement(ManagementSystem):

    def __init__(self, storage_handler):
        super().__init__("Orders", "Order Management", storage_handler)

    def create_new_order(self, item_list, total_cost, address, status, username, date):
        key_list = list(self._db.keys())
        unique_id = uuid.uuid4()

        while True:
            if unique_id in key_list:
                unique_id = uuid.uuid4()
            else:
                break

        new_order = Order(item_list, total_cost, address, status, username, date, unique_id)

        self._db[unique_id] = new_order
        self._handler.set_storage(self._key_name, self._db)
        print("adding new order: {}".format(new_order.get_orderID()))

    def retrieve_all_order_id(self):
        key_list = list(self._db.keys())

        if key_list == []:

            return None

        else:
            return key_list



