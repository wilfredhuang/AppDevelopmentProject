class Order:
    def __init__(self):
        # // FIRST SECTION
        self.__orderID = ""
        self.__deliveryType = ""
        self.__orderDate = ""
        self.__paymentMethod = ""
        self.__authCode = ""
        self.__eta = ""
        # // THIRD SECTION
        self.__paymentStageUI = ""
        # // FOURTH SECTION
        self.__order_log = {}
        self.__order_log_comment = 1
        # // FIFTH SECTION
        # // SHIPPING ADDRESS
        self.__userFullName = ""
        self.__userAddress = ""
        self.__userAddressFloor = ""
        self.__userPostalCode = ""
        # // TOTAL SUMMARY
        self.__subtotal = ""
        self.__shippingFee = ""
        self.__total = ""

        # // MUTATOR METHODS

        # // FIRST SECTION
    def set_orderID(self, orderID):
        self.__orderID = orderID

    def set_deliveryType(self, deliveryType):
        self.__deliveryType = deliveryType

    def set_orderDate(self, orderDate):
        self.__orderDate = orderDate

    def set_paymentMethod(self, paymentMethod):
        self.__paymentMethod = paymentMethod

    def set_authCode(self, authCode):
        self.__authCode = authCode

    def set_eta(self, eta):
        self.__eta = eta

    # // THIRD SECTION

    # // FOURTH SECTION
    # Order Log Section

    def add_comment(self, time, comment):
        self.__order_log[self.__order_log_comment] = [time, comment]
        self.__order_log_comment += 1

    def get_order_log(self):
        return self.__order_log

    def get_order_log_time(self, commentnumber):
        return self.__order_log[commentnumber][0]

    def get_order_log_comment(self, commentnumber):
        return self.__order_log[commentnumber][1]

    # // FIFTH SECTION
    # // SHIPPING ADDRESS

    def set_userFullName(self, userFullName):
        self.__userFullName = userFullName

    def set_userAddress(self, userAddress):
        self.__userAddress = userAddress

    def set_userAddressFloor(self, userAddressFloor):
        self.__userAddressFloor = userAddressFloor

    def set_userPostalCode(self, userPostalCode):
        self.__userPostalCode = userPostalCode

    # // TOTAL SUMMARY
    def set_subtotal(self, subtotal):
        self.__subtotal = subtotal

    def set_shippingFee(self, shippingFee):
        self.__shippingFee = shippingFee

    def set_total(self, total):
        self.__total = total

    # // GET METHODS

    # // TOP SECTION
    def get_orderID(self):
        return self.__orderID

    def get_deliveryType(self):
        return self.__deliveryType

    def get_orderDate(self):
        return self.__orderDate

    def get_paymentMethod(self):
        return self.__paymentMethod

    def get_authCode(self):
        return self.__authCode

    def get_eta(self):
        return self.__eta

    # // THIRD SECTION

    # // BOTTOM SECTION
    # // SHIPPING ADDRESS

    def get_userFullName(self):
        return self.__userFullName

    def get_userAddress(self):
        return self.__userAddress

    def get_userAddressFloor(self):
        return self.__userAddressFloor

    def get_userPostalCode(self):
        return self.__userPostalCode

    # // TOTAL SUMMARY.
    def get_subtotal(self):
        return self.__subtotal

    def get_shippingFee(self):
        return self.__shippingFee

    def get_total(self):
        return self.__total

    def __str__(self):
        return "This is order #" + str(individual_order.get_orderID)


individual_order = Order()
individual_order.set_orderID("1")
individual_order.set_deliveryType("Standard")
individual_order.set_orderDate("11 Dec 12:45:28")
individual_order.set_paymentMethod("****-1234")
individual_order.set_authCode("123456")
individual_order.set_eta("Sat 15 Dec - Tue 17 Dec")
individual_order.set_userFullName("John Lim")
individual_order.set_userAddress("Blk 123 Sesame Street")
individual_order.set_userAddressFloor("#10-1337")
individual_order.set_userPostalCode("Singapore, 123456")
individual_order.set_subtotal("119.98")
individual_order.set_shippingFee("0.00")
individual_order.set_total("119.98")
individual_order.add_comment("01/02/20", "First Comment")
individual_order.add_comment("02/02/20", "Second Comment")
individual_order.add_comment("03/02/20", "Third Comment")
print(individual_order.get_order_log())