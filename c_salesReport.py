"""
Sales Report class:

handle monthly/ daily report
contains all info need for a single report

"""

class CSalesReport:

    def __init__(self, type):

        if (type == 'm' or type == 'M'):
            self.reportType = "monthly"
        elif (type == 'd' or type == 'D'):
            self.reportType = "daily"
        elif (type == 'y' or type == 'Y'):
            self.reportType = "yearly"

        self.salesAmount = 0.0
        self.quantitySold = 0
        self.numTransaction = 0.0


    def getReportType(self):

        return self.reportType

    def getSalesAmount(self):

        return  self.salesAmount

    def getQuantitySold(self):

        return self.quantitySold

    def addQuantity(self, quantity):

        self.quantitySold += quantity

    def addSalesAmount(self, salesAmount):

        self.salesAmount += salesAmount

    def increaseNumTransaction(self):

        self.numTransaction += 1