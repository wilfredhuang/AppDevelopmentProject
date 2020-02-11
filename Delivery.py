class Delivery:
    def __init__(self, orderID, orderDate, receiver_name, deliveryType, remarks):
        self.__orderID = orderID
        self.__orderDate = orderDate
        self.__receiver_name = receiver_name
        self.__deliveryType = deliveryType
        self.__remarks = remarks

    # Mutator Methods

    def set_orderID(self, orderID):
        self.__orderID = orderID

    def set_orderDate(self, orderDate):
        self.__orderDate = orderDate

    def set_receiver_name(self, receiver_name):
        self.__receiver_name = receiver_name

    def set_deliveryType(self, deliveryType):
        self.__deliveryType = deliveryType

    def set_remarks(self, remarks):
        self.__remarks = remarks

    # Accessor Methods

    def get_orderID(self):
        return self.__orderID

    def get_orderDate(self):
        return self.__orderDate

    def get_receiver_name(self):
        return self.__receiver_name

    def get_deliveryType(self):
        return self.__deliveryType

    def get_remarks(self):
        return self.__remarks