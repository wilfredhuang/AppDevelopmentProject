"""
Add delivery
Modify delivery
Retrieve delivery
delete delivery
"""


from ManagementSystem import ManagementSystem
from Delivery import Delivery
import uuid


class DeliveryManagement(ManagementSystem):
    def __init__(self, storage_handler):
        super().__init__("Delivery", "Delivery Management", storage_handler)

    def create_new_delivery(self, orderID, orderDate, receiver_name, deliveryType, remarks):
        key_list = list(self._db.keys())
        unique_id = uuid.uuid4()

        while True:
            if unique_id in key_list:
                unique_id = str(uuid.uuid4())
            else:
                break
        new_delivery = Delivery(orderID, orderDate, receiver_name, deliveryType, remarks)

        self._db[unique_id] = new_delivery
        self._handler.set_storage(self._key_name, self._db)

        print("Testing delivery.....", self._db)
        print("adding new delivery: {}".format(new_delivery.get_orderID()))

    def update_delivery(self):
        pass


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



