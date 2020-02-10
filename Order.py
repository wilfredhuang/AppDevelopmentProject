class Order:

    def __init__(self, item_list, productPrice, address, status, username, date, unique_id):
        self.__orderID = unique_id
        self.__item_list = item_list
        self.__productPrice = productPrice
        self.__address = address
        self.__status = status
        self.__username = username
        self.__date = date
        #
        self.__order_eta = "5"
        self.__order_log = {}
        self.__order_log_comment = 1
        self.__deliveryType = "Standard"
        self.__paymentMethod = "Paypal"
        self.__userUnitNumber = "#09-1784"
        self.__userPostalCode = "350155"
        self.__shippingFee = float(5.99)
        self.__subtotal = float(self.__productPrice) - (self.__shippingFee)
        self.__total = self.__subtotal + self.__shippingFee

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

    #
    def get_order_eta(self):
        return self.__order_eta

    def get_order_log(self):
        return self.__order_log

    def get_order_log_time(self, commentnumber):
        return self.__order_log[commentnumber][0]

    def get_order_log_comment(self, commentnumber):
        return self.__order_log[commentnumber][1]

    def get_deliveryType(self):
        return self.__deliveryType

    def get_paymentMethod(self):
        return self.__paymentMethod

    def get_userUnitNumber(self):
        return self.__userUnitNumber

    def get_userPostalCode(self):
        return self.__userPostalCode

    def get_subtotal(self):
        return self.__subtotal

    def get_shippingFee(self):
        return self.__shippingFee

    def get_total(self):
        return self.__total

    def add_comment(self, time, comment):
        self.__order_log[self.__order_log_comment] = [time, comment]
        self.__order_log_comment += 1

