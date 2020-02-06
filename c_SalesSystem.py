#import c_salesReport as sr

"""
Sales System class:

handling all sales made
generating sales report
storing data to the sales data storage


"""
"""
class CSalesSystem:

    def __init__(self):
        self.totalSales = 0.00
        self.totalQuantitySold = 0
        self.year = {}
        self.getSalesDataFromStorage()

    def getSalesDataFromStorage(self):
        try:

            with open("SalesData.txt") as f:

                for line in f:

                    line = line.strip()
                    salesdata = line.split(',')

                    # date | ISBN | name | author | price | quantity - txt
                    tempBook = Bk.CBook(salesdata[2], int(salesdata[1]), salesdata[3], float(salesdata[4]), int(salesdata[5]))
                    self.addSales(tempBook, int(salesdata[5]), salesdata[0], True)

            print("\n")
        except IndexError:
            print("##################################")
            print("ERRRORRRRRRRR DO NOT IGNORE THIS!!!!!!! ")
            print("Make sure there is no blank lines in text file, shut down the programme and remove the blank link then try again.")
            print("##################################")

    def getDailySales(self):

        while True:

            date = input('Enter the day, month and year (DD/MM/YYYY): \n')

            if(vc.dateChecker(date)):

                break

            else:
                print("Invalid date, try again!")


        year_Key = int(date[6:])
        month_Key = int(date[3:5])
        day_Key = int(date[:2])

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

    def addSales(self, book, quantitySold, date, fromStorage):

        # Total sales
        self.totalQuantitySold += quantitySold
        self.totalSales += book.getPrice() * quantitySold

        year_Key = int(date[6:])
        month_Key = int(date[3:5])
        day_Key = int(date[:2])

        book_temp = Bk.CBook(book.getName(), book.getISBN(), book.getAuthor(), book.getPrice(), quantitySold)

        if(year_Key in self.year):

            # if there is no sales before in the month
            if(self.year[year_Key][month_Key] == None):

                self.year[year_Key][month_Key] = [None]*32
                self.year[year_Key][month_Key][0] = sr.CSalesReport('m')
                self.year[year_Key][month_Key][day_Key] = [sr.CSalesReport('d'), book_temp]

                if(fromStorage == False):

                    f = open("SalesData.txt", 'a')
                    f.write(date + ',' + str(book.getISBN()) + ',' + book.getName() + ',' + book.getAuthor() + ',' + str(
                        book.getPrice()) + ',' + str(quantitySold) + "\n")
                    f.close()

            # if there is sales before in the month but no on that day
            elif(self.year[year_Key][month_Key][day_Key] == None):

                self.year[year_Key][month_Key][day_Key] = [sr.CSalesReport('d'), book_temp]

                if(fromStorage == False):

                    f = open("SalesData.txt", 'a')
                    f.write(date + ',' + str(book.getISBN()) + ',' + book.getName() + ',' + book.getAuthor() + ',' + str(
                        book.getPrice()) + ',' + str(quantitySold) + "\n")
                    f.close()

            # if there is sales in that day before
            else:

                duplicate_book = False

                for i in range(1, self.year[year_Key][month_Key][day_Key].__len__()):

                    if(self.year[year_Key][month_Key][day_Key][i].getISBN() == book.getISBN()):
                        duplicate_book = True
                        self.year[year_Key][month_Key][day_Key][i].addQuantity(quantitySold)

                        if(fromStorage == False):

                            f = open("SalesData.txt", 'a')
                            f.write(
                                date + ',' + str(
                                    book.getISBN()) + ',' + book.getName() + ',' + book.getAuthor() + ',' + str(
                                    book.getPrice()) + ',' + str(quantitySold) + "\n")
                            f.close()

                if(duplicate_book == False):
                    self.year[year_Key][month_Key][day_Key].append(book_temp)

                    if(fromStorage == False):

                        f = open("SalesData.txt", 'a')
                        f.write(
                            date + ',' + str(book.getISBN()) + ',' + book.getName() + ',' + book.getAuthor() + ',' + str(
                                book.getPrice()) + ',' + str(quantitySold) + "\n")
                        f.close()

            # yearly sales report
            self.year[year_Key][0].addQuantity(quantitySold)
            self.year[year_Key][0].addSalesAmount(book.getPrice() * quantitySold)

            # monthly sales report
            self.year[year_Key][month_Key][0].addQuantity(quantitySold)
            self.year[year_Key][month_Key][0].addSalesAmount(book_temp.getPrice() * quantitySold)
            self.year[year_Key][month_Key][0].increaseNumTransaction()

            # daily sales report
            self.year[year_Key][month_Key][day_Key][0].addQuantity(quantitySold)
            self.year[year_Key][month_Key][day_Key][0].addSalesAmount(book_temp.getPrice() * quantitySold)
            self.year[year_Key][month_Key][day_Key][0].increaseNumTransaction()

        else:

            # append to current list of books sold
            self.year[year_Key] = [None]*13
            self.year[year_Key][month_Key] = [None]*32
            self.year[year_Key][month_Key][day_Key] = [sr.CSalesReport('d'), book_temp]

            # daily sales report
            self.year[year_Key][month_Key][day_Key][0].addQuantity(quantitySold)
            self.year[year_Key][month_Key][day_Key][0].addSalesAmount(book_temp.getPrice() * quantitySold)
            self.year[year_Key][month_Key][day_Key][0].increaseNumTransaction()

            # yearly sales report
            self.year[year_Key][0] = sr.CSalesReport('y')
            self.year[year_Key][0].addQuantity(quantitySold)
            self.year[year_Key][0].addSalesAmount(book_temp.getPrice() * quantitySold)
            self.year[year_Key][0].increaseNumTransaction()

            # monthly sales report
            self.year[year_Key][month_Key][0] = sr.CSalesReport('m')
            self.year[year_Key][month_Key][0].addQuantity(quantitySold)
            self.year[year_Key][month_Key][0].addSalesAmount(book_temp.getPrice() * quantitySold)
            self.year[year_Key][month_Key][0].increaseNumTransaction()

            if(fromStorage == False):

                f = open("SalesData.txt", 'a')
                f.write(date + ',' + str(book.getISBN()) + ',' + book.getName() + ',' + book.getAuthor() + ',' + str(book.getPrice()) + ',' + str(quantitySold) + "\n")
                f.close()




    def updateDailySales(self):
        pass
    def updateMonthlySales(self):
        pass
    def updateYearlySales(self):
        pass
        
        
"""