from c_SalesReport import CSalesReport
from ManagementSystem import ManagementSystem
"""
HF
Sales System class:

handling all sales made
generating sales report
storing data to the sales data storage

date format: YYYY-MM-DD
Parameter: order class
"""


class SalesManagement(ManagementSystem):

    def __init__(self, storage_handler):
        super().__init__("Sales", "Sales Management", storage_handler)
        self.__overall_sales_report = CSalesReport()

    def get_report(self, day, month, year):
        print("getting report from {}-{}-{}".format(year, month, day))
        if(year in self._db):

            # if there is no sales found in the month before
            if (self._db[year][month] == None):

                return None

            # if there is sales before in the month but not on that day
            elif (self._db[year][month][day] == None):

                return None
            else:
                print("report found")
                return self._db[year][month][day]

        else:
            return None

    """
    def getDailySales(self):

        while True:

            date = input('Enter the day, month and year (DD/MM/YYYY): \n')

            if(vc.dateChecker(date)):

                break

            else:
                print("Invalid date, try again!")


        year_Key = int(date[:4])
        month_Key = int(date[5:7])
        day_Key = int(date[8:])

        if (year_Key in self.year):

            if (self.year[year_Key][month_Key] == None):
                print("There's no sales in that month {} of the year {}".format(month_Key, year_Key))

            else:

                if(self.year[year_Key][month_Key][day_Key] == None):

                    print("No sales found on that day {}".format(date))

                else:
                    print("************************************ SALES REPORT ************************************")
                    print("Report for: {}".format(date))
                    print("Total amount of books sold that day is {}".format(self.year[year_Key][month_Key][day_Key][0].getQuantitySold()))
                    print("You have gain ${:.2f} from the sales on that day".format(self.year[year_Key][month_Key][day_Key][0].getSalesAmount()))

                    print("\n")
                    print("Total books sold overall: {}".format(self.totalQuantitySold))
                    print("Total sales earned overall: ${:.2f}".format(self.totalSales))
                    print("\n")

                    print("Showing all books sold that day: \n")

                    for i in self.year[year_Key][month_Key][day_Key][1:]:

                        print("You have sold {} of book: '{}' \n".format(i.getQuantity(), i.getName()))

                    print("**************************************** END ******************************************")


        else:

            print("There's no sales at all in the year {}".format(year_Key))

    def getMonthlySales(self):

        while True:

            date = input('Enter month and year (MM/YYYY): \n')
            if (vc.monthYearChecker(date)):
                break
            else:
                print("Invalid date, try again!")

        year_Key = int(date[3:])
        month_Key = int(date[:2])

        if (year_Key in self.year):

            if(self.year[year_Key][month_Key] == None):
                print("There's no sales in that month {} of the year {}".format(month_Key, year_Key))

            else:

                print("************************************ SALES REPORT ************************************")
                print("Report for: {}".format(date))
                print("Total amount of books sold that month is {}".format(self.year[year_Key][month_Key][0].getQuantitySold()))
                print("You have gain ${:.2f} from the sales in that month".format(self.year[year_Key][month_Key][0].getSalesAmount()))

                print("\n")
                print("Total books sold overall: {}".format(self.totalQuantitySold))
                print("Total sales earned from overall: ${:.2f}".format(self.totalSales))
                print("\n")
                print("**************************************** END ******************************************")

        else:

            print("There's no sales at all in the year {}".format(year_Key))

    def getYearlySales(self):

        while True:

            date = input('Enter year (YYYY): \n')
            if (vc.yearChecker(date)):
                break
            else:
                print("Invalid date, try again!")

        year_Key = int(date)

        if (year_Key in self.year):


            print("************************************ SALES REPORT ************************************")
            print("Report for year {} ".format(date))
            print("Total amount of books sold that year is {}".format(self.year[year_Key][0].getQuantitySold()))
            print("You have gain ${:.2f} from the sales in that year".format(self.year[year_Key][0].getSalesAmount()))

            print("\n")
            print("Total books sold overall: {}".format(self.totalQuantitySold))
            print("Total sales earned from overall: ${:.2f}".format(self.totalSales))
            print("\n")
            print("**************************************** END ******************************************")

        else:

            print("There's no sales at all in the year {}".format(year_Key))

    def showSales(self):

        while True:

            reportType = input("Choose Monthly or Daily report (D/M/Y): \n")

            if(reportType == 'd' or reportType == 'D'):

                self.getDailySales()
                break

            elif(reportType == 'M' or reportType == 'm'):

                self.getMonthlySales()
                break

            elif(reportType == 'Y' or reportType == 'y'):

                self.getYearlySales()
                break
            else:

                print("Enter properly leh")
    
    """
    def add_sales(self, item_list, date):

        # Total sales
        if item_list == []:

            print("UNABLE TO UPDATE OVERALL SALES DUE TO PARAMETER: (item_list) Empty")

        else:
            print("updating overall sales")
            self.__overall_sales_report.add_items(item_list)

        temp_date = str(date)

        year_key = int(temp_date[:4])
        month_key = int(temp_date[5:7])
        day_key = int(temp_date[8:])

        print("updating {} {} {}".format(year_key, month_key, day_key))
        # if sales found in that year before
        if(year_key in self._db):

            # if there is no sales found in the month before
            if(self._db[year_key][month_key] == None):

                self._db[year_key][month_key] = [None]*32
                # create sales report for month
                self._db[year_key][month_key][0] = CSalesReport()
                # create sales report for day
                self._db[year_key][month_key][day_key] = CSalesReport()

            # if there is sales before in the month but not on that day
            elif(self._db[year_key][month_key][day_key] == None):

                self._db[year_key][month_key][day_key] = CSalesReport()

            # daily sales report
            self._db[year_key][month_key][day_key].add_items(item_list)

            # monthly sales report
            self._db[year_key][month_key][0].add_items(item_list)

            # yearly sales report
            self._db[year_key][0].add_items(item_list)

        # if no sales found in that year
        else:

            # append to current list of books sold
            self._db[year_key] = [None]*13
            self._db[year_key][month_key] = [None]*32
            self._db[year_key][month_key][day_key] = CSalesReport()

            # daily sales report
            self._db[year_key][month_key][day_key].add_items(item_list)

            # monthly sales report
            self._db[year_key][month_key][0] = CSalesReport()
            self._db[year_key][month_key][0].add_items(item_list)

            # yearly sales report
            self._db[year_key][0] = CSalesReport()
            self._db[year_key][0].add_items(item_list)

        self._handler.set_storage(self._key_name, self._db)
