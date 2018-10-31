import sys
import sqlite3
import csv

from os import listdir
from os.path import isfile, join
from datetime import datetime

def getStockTickersFromPriceFolder(stockPricesFolder):
    stockTickers = []
    filesInPriceFolder = [file for file in listdir(stockPricesFolder) if isfile(join(stockPricesFolder, file))]
    for currFile in filesInPriceFolder:
        tempFilename = currFile.replace(".csv", "")
        tempFilename = tempFilename.replace(".CSV", "")
        stockTickers.append(tempFilename)

    return stockTickers

def getInvestmentTypeId(dbCurs, investmentType):
    getInvestmentTypeIdSQL = "SELECT investment_type_id FROM investment_types WHERE investment_type_title = ?"
    dbCurs.execute(getInvestmentTypeIdSQL, [investmentType])
    currentRows = dbCurs.fetchall()
    investmentTypeId = currentRows[0][0]
    
    return investmentTypeId
    
def stockInDB(dbCurs, stockTicker):
    checkStockTicker = "SELECT COUNT(*) FROM investments WHERE investment_abbreviation = ?"
    dbCurs.execute(checkStockTicker, [stockTicker])
    currentRows = dbCurs.fetchall()
    if currentRows[0][0] > 0:
        return True
    return False
    
def addStock(dbConn, dbCurs, investmentTypeId, stockTicker):
    checkStockPrice = "INSERT INTO investments (investment_title, investment_type_id, investment_abbreviation, date_added, date_updated)"
    checkStockPrice += " VALUES (?, ?, ?, ?, ?)"
    now = datetime.now()
    dbCurs.execute(checkStockPrice, (stockTicker, investmentTypeId, stockTicker, now, now))
    dbConn.commit()
    
def getInvestmentId(dbCurs, stockTicker):
    investmentId = -999
    if not stockInDB(dbCurs, stockTicker):
        investmentTypeId = getInvestmentTypeId(dbCurs, "Stocks")
        addStock(dbConn, dbCurs, investmentTypeId, stockTicker)
    getInvestmentIdSQL = "SELECT investment_id FROM investments WHERE investment_abbreviation = ?"
    dbCurs.execute(getInvestmentIdSQL, [stockTicker])
    currentRows = dbCurs.fetchall()
    investmentId = currentRows[0][0]
    
    return investmentId

def stockPriceInDB(dbCurs, investmentId, dayOfPrice):
    checkStockPrice = "SELECT COUNT(*) FROM stock_prices WHERE investment_id = ? AND day_of_price = ?"
    dbCurs.execute(checkStockPrice, (investmentId, dayOfPrice))
    currentRows = dbCurs.fetchall()
    if currentRows[0][0] > 0:
        return True
    return False
    
def addStockPrice(dbConn, dbCurs, investmentId, dayOfPrice, openPrice, highPrice, lowPrice, closePrice, adjClosePrice, volume):
    if stockPriceInDB(dbCurs, investmentId, dayOfPrice):
        return
    checkStockPrice = "INSERT INTO stock_prices (investment_id, day_of_price, open_price, high_price"
    checkStockPrice += ", low_price, close_price, adjusted_close_price, volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    dbCurs.execute(checkStockPrice, (investmentId, dayOfPrice, openPrice, highPrice, lowPrice, closePrice, adjClosePrice, volume))
    dbConn.commit()
    
def addStockPricesFromFile(dbConn, dbCurs, investmentId, stockPricesCSV):
    with open(stockPricesCSV, newline='') as csvFile:
        stockPriceReader = csv.reader(csvFile, delimiter=',', quotechar='"')
        for currentRow in stockPriceReader:
            if currentRow[0] != 'Date' and currentRow[0] != '':
                (dayOfPrice, openPrice, highPrice, lowPrice, closePrice, adjClosePrice, volume) = currentRow
                addStockPrice(dbConn, dbCurs, investmentId, dayOfPrice, openPrice, highPrice, lowPrice, closePrice, adjClosePrice, volume)



stockDB = 'stockData.db'
dbConn = sqlite3.connect(stockDB)
dbCurs = dbConn.cursor()

stockPricesFolder = 'F:/0_data_is_in_here_0/softwareDev/aiResearch/datasets/Stocks/yahoo_finance/'

stockTickers = getStockTickersFromPriceFolder(stockPricesFolder)
for currStockTicker in stockTickers:
    print("Adding stock ticker information (%s)" % (currStockTicker))
    stockPricesCSV = stockPricesFolder + currStockTicker + '.csv'
    investmentId = getInvestmentId(dbCurs, currStockTicker)
    addStockPricesFromFile(dbConn, dbCurs, investmentId, stockPricesCSV)

dbConn.close()
