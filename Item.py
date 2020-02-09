class Item():
    def __init__(self, id, name, cost, image_name):
        self.__id = str(id)
        self.__name = name
        self.__cost = cost
        self.__image_file = image_name
        self.__quantity = 1
        self.__stock = 0

    def add_quantity(self):
        self.__quantity += 1

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_cost(self):
        return self.__cost

    def set_cost(self, cost):
        self.__cost = cost

    def get_file(self):
        return self.__image_file

    def get_quantity(self):
        return self.__quantity

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def get_stock(self):
        return self.__stock

    def set_stock(self, stock):
        self.__stock = int(stock)


class Wired(Item):
    def __init__(self, id, name, cost, image_name):
        super(Wired, self).__init__(id, name, cost, image_name)
        self.__type = "W"

    def get_type(self):
        return self.__type


class Wireless(Item):
    def __init__(self, id, name, cost, image_name):
        super(Wireless, self).__init__(id, name, cost, image_name)
        self.__type = "WL"

    def get_type(self):
        return self.__type
