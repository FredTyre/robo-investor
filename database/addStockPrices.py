#########################################################################################
# Author : Fred Tyre (aka One5hot76)                                                    #
# See main folder for LICENSE and README files related to this open source project      #
# Gentle reminder to use at your own risk! Absolutely no warranty is implied with       #
# this product as stated in Readme file in main folder.                                 #
#########################################################################################

import sqlite3
import investmentDBLibrary

stockDB = 'stockData.db'
dbConn = sqlite3.connect(stockDB)
dbCurs = dbConn.cursor()

stockPricesFolder = 'F:/0_data_is_in_here_0/softwareDev/aiResearch/datasets/Stocks/yahoo_finance/'

stockTickers = investmentDBLibrary.getStockTickersFromPriceFolder(stockPricesFolder)
for currStockTicker in stockTickers:
    print("Adding stock ticker information (%s)" % (currStockTicker))
    stockPricesCSV = stockPricesFolder + currStockTicker + '.csv'
    investmentId = investmentDBLibrary.getInvestmentId(dbConn, dbCurs, currStockTicker)
    investmentDBLibrary.addStockPricesFromFile(dbConn, dbCurs, investmentId, stockPricesCSV)

dbConn.close()
