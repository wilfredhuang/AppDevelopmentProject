class Order:
    countID = 0
    def __init__(self, item_list, productPrice, address, status, username, date):
        Order.countID += 1
        self.__item_list = item_list
        self.__productPrice = productPrice
        #self.__orderID = orderID
        self.__address = address
        self.__status = status
        self.__username = username
        self.__date = date

    def get_item_list(self):
        return self.__item_list

    def get_productPrice(self):
        return self.__productPrice

    def get_orderID(self):
        return self.__orderID

    def get_address(self):
        return self.__address

    def get_status(self):
        return self.__status

    def get_username(self):
        return self.__username

    def get_date(self):
        return self.__date

    def set_item_list(self, item_list):
        self.__item_list = item_list

    def set_productPrice(self, productPrice):
        self.__productPrice = productPrice

    def set_orderID(self, orderID):
        self.__orderID = orderID

    def set_address(self, address):
        self.__address = address

    def set_status(self, status):
        self.__status = status

    def set_username(self, username):
        self.__username = username

    def set_date(self, date):
        self.__date = date
