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
    investmentId = investmentDBLibrary.getInvestmentId(dbCurs, currStockTicker)
    investmentDBLibrary.addStockPricesFromFile(dbConn, dbCurs, investmentId, stockPricesCSV)

dbConn.close()
