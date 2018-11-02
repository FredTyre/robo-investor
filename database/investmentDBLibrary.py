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

def stockPriceDiffInDB(dbCurs, investmentId, dayOfPrice):
    checkStockPriceDiff = "SELECT COUNT(*) FROM stock_price_diffs WHERE investment_id = ? AND day_of_price = ?"
    dbCurs.execute(checkStockPriceDiff, (investmentId, dayOfPrice))
    currentRows = dbCurs.fetchall()
    if currentRows[0][0] > 0:
        return True
    return False

def stockPriceDiffPercInDB(dbCurs, investmentId, dayOfPrice):
    checkStockPriceDiffPerc = "SELECT COUNT(*) FROM stock_price_diff_percs WHERE investment_id = ? AND day_of_price = ?"
    dbCurs.execute(checkStockPriceDiffPerc, (investmentId, dayOfPrice))
    currentRows = dbCurs.fetchall()
    if currentRows[0][0] > 0:
        return True
    return False
    
def addStockPrice(dbConn, dbCurs, investmentId, dayOfPrice, openPrice, highPrice, lowPrice, closePrice, adjClosePrice, volume):
    if stockPriceInDB(dbCurs, investmentId, dayOfPrice):
        return
    addStockPrice = "INSERT INTO stock_prices (investment_id, day_of_price, open_price, high_price"
    addStockPrice += ", low_price, close_price, adjusted_close_price, volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    dbCurs.execute(addStockPrice, (investmentId, dayOfPrice, openPrice, highPrice, lowPrice, closePrice, adjClosePrice, volume))
    dbConn.commit()

def addStockPriceDiff(dbConn, dbCurs, investmentId, dayOfPrice, openPriceDiff, highPriceDiff, lowPriceDiff, closePriceDiff, adjClosePriceDiff, volumeDiff):
    if stockPriceDiffInDB(dbCurs, investmentId, dayOfPrice):
        return
    addStockPriceDiff = "INSERT INTO stock_price_diffs (investment_id, day_of_price, open_price_diff, high_price_diff"
    addStockPriceDiff += ", low_price_diff, close_price_diff, adj_close_price_diff, volume_diff) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    dbCurs.execute(addStockPriceDiff, (investmentId, dayOfPrice, openPriceDiff, highPriceDiff, lowPriceDiff, closePriceDiff, adjClosePriceDiff, volumeDiff))
    dbConn.commit()

def addStockPriceDiffPerc(dbConn, dbCurs, investmentId, dayOfPrice, openPriceDiffPerc, highPriceDiffPerc, lowPriceDiffPerc, closePriceDiffPerc, adjClosePriceDiffPerc, volumeDiffPerc):
    if stockPriceDiffPercInDB(dbCurs, investmentId, dayOfPrice):
        return
    addStockPriceDiff = "INSERT INTO stock_price_diff_percs (investment_id, day_of_price, open_price_diff_perc, high_price_diff_perc"
    addStockPriceDiff += ", low_price_diff_perc, close_price_diff_perc, adj_close_price_diff_perc, volume_diff_perc) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    dbCurs.execute(addStockPriceDiff, (investmentId, dayOfPrice, openPriceDiffPerc, highPriceDiffPerc, lowPriceDiffPerc, closePriceDiffPerc, adjClosePriceDiffPerc, volumeDiffPerc))
    dbConn.commit()

def addStockPricesFromFile(dbConn, dbCurs, investmentId, stockPricesCSV):
    with open(stockPricesCSV, newline='') as csvFile:
        stockPriceReader = csv.reader(csvFile, delimiter=',', quotechar='"')
        for currentRow in stockPriceReader:
            if currentRow[0] != 'Date' and currentRow[0] != '':
                (dayOfPrice, openPrice, highPrice, lowPrice, closePrice, adjClosePrice, volume) = currentRow
                addStockPrice(dbConn, dbCurs, investmentId, dayOfPrice, openPrice, highPrice, lowPrice, closePrice, adjClosePrice, volume)
    genStockPriceDifferences(dbConn, dbCurs, investmentId)

def getStockPricesFromDB(dbConn, dbCurs, investmentId):
    getStockPrices = "SELECT * FROM stock_prices WHERE investment_id = ? ORDER BY day_of_price"
    dbCurs.execute(getStockPrices, [investmentId])
    stockPrices = dbCurs.fetchall()
    return stockPrices

def genStockPriceDifferences(dbConn, dbCurs, investmentId):
    stockPriceDiffs = []
    stockPriceDiffPercs = []
    stockPrices = getStockPricesFromDB(dbConn, dbCurs, investmentId)
    numStockPrices = len(stockPrices)
    for stockPriceCounter in range(numStockPrices):
        if stockPriceCounter > 0:
            (prevInvestmentIdDB, prevDayOfPrice, prevOpenPrice, prevHighPrice, prevLowPrice, prevClosePrice, prevAdjClosePrice, prevVolume) = stockPrices[stockPriceCounter - 1]
            (investmentIdDB, dayOfPrice, openPrice, highPrice, lowPrice, closePrice, adjClosePrice, volume) = stockPrices[stockPriceCounter]

            if prevOpenPrice == "null":
                prevOpenPrice = 0
            if prevHighPrice == "null":
                prevHighPrice = 0
            if prevLowPrice == "null":
                prevLowPrice = 0
            if prevClosePrice == "null":
                prevClosePrice = 0
            if prevAdjClosePrice == "null":
                prevAdjClosePrice = 0
            if prevVolume == "null":
                prevVolume = 0
            
            if openPrice == "null":
                openPrice = 0
            if highPrice == "null":
                highPrice = 0
            if lowPrice == "null":
                lowPrice = 0
            if closePrice == "null":
                closePrice = 0
            if adjClosePrice == "null":
                adjClosePrice = 0
            if volume == "null":
                volume = 0

            openPriceDiff = float(openPrice) - float(prevClosePrice)
            highPriceDiff = float(highPrice) - float(prevClosePrice)
            lowPriceDiff = float(lowPrice) - float(prevClosePrice)
            closePriceDiff = float(closePrice) - float(prevClosePrice)
            adjClosePriceDiff = float(adjClosePrice) - float(prevAdjClosePrice)
            volumeDiff = float(volume) - float(prevVolume)

            if prevClosePrice == 0:
                openPriceDiffPerc = (float(openPrice) - float(prevClosePrice)) * 100 / 0.000001
                highPriceDiffPerc = (float(highPrice) - float(prevClosePrice)) * 100 / 0.000001
                lowPriceDiffPerc = (float(lowPrice) - float(prevClosePrice)) * 100 / 0.000001
                closePriceDiffPerc = (float(closePrice) - float(prevClosePrice)) * 100 / 0.000001
            else:
                openPriceDiffPerc = (float(openPrice) - float(prevClosePrice)) * 100 / float(prevClosePrice)
                highPriceDiffPerc = (float(highPrice) - float(prevClosePrice)) * 100 / float(prevClosePrice)
                lowPriceDiffPerc = (float(lowPrice) - float(prevClosePrice)) * 100 / float(prevClosePrice)
                closePriceDiffPerc = (float(closePrice) - float(prevClosePrice)) * 100 / float(prevClosePrice)
            
            if prevAdjClosePrice == 0:
                adjClosePriceDiffPerc = (float(adjClosePrice) - float(prevAdjClosePrice)) * 100 / 0.000001
            else:
                adjClosePriceDiffPerc = (float(adjClosePrice) - float(prevAdjClosePrice)) * 100 / float(prevAdjClosePrice)
                
            if prevVolume == 0:
                volumeDiffPerc = (float(volume) - float(prevVolume)) * 100 / 0.0001
            else:
                volumeDiffPerc = (float(volume) - float(prevVolume)) * 100 / float(prevVolume)
            
            stockPriceDiffs.append((dayOfPrice, openPriceDiff, highPriceDiff, lowPriceDiff, closePriceDiff, adjClosePriceDiff, volumeDiff))
            stockPriceDiffPercs.append((dayOfPrice, openPriceDiffPerc, highPriceDiffPerc, lowPriceDiffPerc, closePriceDiffPerc, adjClosePriceDiffPerc, volumeDiffPerc))
        else:
            (investmentIdDB, dayOfPrice, openPrice, highPrice, lowPrice, closePrice, adjClosePrice, volume) = stockPrices[stockPriceCounter]
            stockPriceDiffs.append((dayOfPrice, 0, 0, 0, 0, 0, 0))
            stockPriceDiffPercs.append((dayOfPrice, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00))

    for currStockPriceDiff in stockPriceDiffs:
        (dayOfPrice, openPriceDiff, highPriceDiff, lowPriceDiff, closePriceDiff, adjClosePriceDiff, volumeDiff) = currStockPriceDiff
        addStockPriceDiff(dbConn, dbCurs, investmentId, dayOfPrice, openPriceDiff, highPriceDiff, lowPriceDiff, closePriceDiff, adjClosePriceDiff, volumeDiff)
    
    for currStockPriceDiffPerc in stockPriceDiffPercs:
        (dayOfPrice, openPriceDiffPerc, highPriceDiffPerc, lowPriceDiffPerc, closePriceDiffPerc, adjClosePriceDiffPerc, volumeDiffPerc) = currStockPriceDiffPerc
        addStockPriceDiffPerc(dbConn, dbCurs, investmentId, dayOfPrice, openPriceDiffPerc, highPriceDiffPerc, lowPriceDiffPerc, closePriceDiffPerc, adjClosePriceDiffPerc, volumeDiffPerc)
    






