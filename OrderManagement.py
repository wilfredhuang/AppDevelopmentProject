"""
HF

OrderManagement in charged to creating orders after payment
Since OrderManagement is directly related to SalesManagement,
SalesManagement will be calling functions of SalesManagement.

Information from payments will be passed here and from here,
Orders will be stored and new sales information will be creteaf

"""

from ManagementSystem import ManagementSystem
from Order import Order
import uuid


class OrderManagement(ManagementSystem):

    def __init__(self, storage_handler, sales_management):
        super().__init__("Orders", "Order Management", storage_handler)
        self.__sales_management = sales_management

    def create_new_order(self, item_list, total_cost, address, status, username, date):
        key_list = list(self._db.keys())
        unique_id = uuid.uuid4()

        while True:
            if unique_id in key_list:
                unique_id = str(uuid.uuid4())
            else:
                break

        print("Making new order object....")
        new_order = Order(item_list, total_cost, address, status, username, date, unique_id)

        print("Adding uniqueid-object pair to db....")
        self._db[unique_id] = new_order
        print("Key name is", self._key_name)
        print("Set storage.....")
        self._handler.set_storage(self._key_name, self._db)

        self.__sales_management.add_sales(item_list, date)


        print("adding new order: {}".format(new_order.get_orderID()))

    def retrieve_all_order_id(self):
        key_list = list(self._db.keys())

        if key_list == []:

            return None

        else:
            return key_list

    def retrieve_order_by_id(self, key):
        key_list = list(self._db.keys())

        if key_list == []:

            return None

        else:
            return self._db[key]
