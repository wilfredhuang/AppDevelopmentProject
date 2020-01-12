class User:
    countID = 0

    def __init__(self, first_name, last_name, username, password, postal_code, address, country, city, unit_number):
        User.countID += 1
        self.__username = username
        self.__firstName = first_name
        self.__lastName = last_name

        self.__password = password
        self.__postal_code = postal_code
        self.__address = address

        self.__country = country
        self.__city = city
        self.__unitNumber = unit_number

    def get_username(self):
        return self.__username

    def get_first_name(self):
        return self.__firstName

    def get_last_name(self):
        return self.__lastName

    def get_password(self):
        return self.__password

    def get_postal_code(self):
        return self.__postal_code

    def get_address(self):
        return self.__address

    def get_country(self):
        return self.__country

    def get_city(self):
        return self.__city

    def get_unit_numbers(self):
        return self.__unitNumber

    def set_username(self, username):
        self.__username = username

    def set_first_name(self, firstName):
        self.__firstName = firstName

    def set_last_name(self, lastName):
        self.__lastName = lastName

    def set_password(self, password):
        self.__password = password

    def set_postal_code(self, postal_code):
        self.__postal_code = postal_code

    def set_address(self, address):
        self.__address = address

    def set__country(self, country):
        self.__country = country

    def set_city(self, city):
        self.__city = city

    def set_unit_number(self, unit_number):
        self.__unitNumber = unit_number

