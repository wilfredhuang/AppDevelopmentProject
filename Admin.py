class Admin():

    def __init__(self, name, password):
        self.__username = name
        self.__password = password
        self.__privilege = True

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password