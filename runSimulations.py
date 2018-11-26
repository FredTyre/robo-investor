import sys
sys.path.insert(0, 'database')

import sqlite3
import investmentDBLibrary

stockDB = 'database/stockData.db'
dbConn = sqlite3.connect(stockDB)
dbCurs = dbConn.cursor()

stockPricesFolder = 'F:/0_data_is_in_here_0/softwareDev/aiResearch/datasets/Stocks/yahoo_finance/'
startDate = '01-01-2018'
endDate = '11-25-2018'
commissionFee = 9.99

stockTickers = investmentDBLibrary.getStockTickersFromPriceFolder(stockPricesFolder)
for currStockTicker in stockTickers:
    print("Running simulation for Stock Ticker (%s) \n   from (%s - %s) \n   with a commission fee of %s dollars." % (currStockTicker, startDate, endDate, commissionFee))
    investmentId = investmentDBLibrary.getInvestmentId(dbConn, dbCurs, currStockTicker)
    investSimTitle = "YTD simulation of daily open purchase for Stock Ticker (%s) from (%s - %s) with a commission fee of %s" % (currStockTicker, startDate, endDate, '$' + str(commissionFee))
    investmentSimId = investmentDBLibrary.addInvestmentSimulation(dbConn, dbCurs, investSimTitle, startDate, endDate, commissionFee)
    

dbConn.close()
