"""
HF
Sales Report class:

handle monthly/ daily report
contains all info need for a single report

"""
from c_IndividualSales import CIndividualSales

class CSalesReport:

    def __init__(self):

        self.__sales_amount = 0.0
        self.__quantity_sold = 0
        self.__num_transaction = 0
        # individual_product : quantity, total sales
        self.__items_sold = {}

    def get_sales_amount(self):
        return self.__sales_amount

    def get_quantity_sold(self):
        return self.__quantity_sold

    def get_num_transaction(self):
        return self.__num_transaction

    def get_popular_item(self):
        temp_quantity = 0
        temp_item = []

        for key, item in self.__items_sold.items():

            if item.quantity_sold > temp_quantity:
                temp_quantity = item.quantity_sold
                temp_item = [key]

            elif item.quantity_sold == temp_quantity:
                temp_item.append(','+key)

        if temp_item == []:
            return None

        else:
            temp = temp_item
            return temp


    def get_profit_item(self):

        temp_profit = 0.0
        temp_item = []

        for key, item in self.__items_sold.items():
            if item.sales_earned > temp_profit:
                temp_profit = item.sales_earned
                temp_item = [key]

            elif item.sales_earned == temp_profit:
                temp_item.append(','+key)

        if temp_item == []:
            return None

        else:
            temp = temp_item
            return temp

    def get_item_sold(self):
        return self.__items_sold

    def add_items(self, item_list):

        for item in item_list:
            if item.get_name() in self.__items_sold:
                self.__items_sold[item.get_name()].sales_earned += int(item.get_quantity()) * float(item.get_cost())
                self.__items_sold[item.get_name()].quantity_sold += int(item.get_quantity())

            else:
                temp = CIndividualSales()
                temp.sales_earned += int(item.get_quantity()) * float(item.get_cost())
                temp.quantity_sold += int(item.get_quantity())
                self.__items_sold[item.get_name()] = temp

            self.__sales_amount += int(item.get_quantity()) * float(item.get_cost())
            self.__quantity_sold += int(item.get_quantity())

        self.__num_transaction += 1




