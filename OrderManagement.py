from ManagementSystem import ManagementSystem


class OrderManagement(ManagementSystem):

    def __init__(self, storage_handler):
        super().__init__("Orders", "Order Management", storage_handler)

    def create_order(self):
        pass

    def get_order(self):
        pass



