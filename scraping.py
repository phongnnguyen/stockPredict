from bs4 import BeautifulSoup as bs
import urllib
import csv
# from datetime import datetime
# from tabulate import tabulate
import scraping
import certifi
import ssl
from settings import SOURCE_WEB,TOKEN_SLACK,CHANNEL
linkUrl = SOURCE_WEB
tokenSlack = TOKEN_SLACK
channel = CHANNEL
class ScrapingWeb():
    def __init__(self, listOfStock,linkUrl,tokenSlack,channel):
        self.listOfStock = listOfStock
        self.linkUrl = linkUrl
        self.tokenSlack = tokenSlack
        self.channel = channel
    def scrapingWEB(self):
        longName = []
        shortName = []
        price = []
        volumn = []
        for stock in self.listOfStock:
            quote_page = self.linkUrl + stock
            gcontext = ssl.SSLContext()
            page = urllib.request.urlopen(quote_page, context=gcontext).read()
            content = bs(page, "html.parser")
            nameStock = content.find('h1').text
            ticker = nameStock[-3:]  # take ticker of stock
            priceStock = content.find('strong', attrs={'id': 'stockname_close'}).text
            volStock = content.find('strong', attrs={'id': 'stockname_volume'}).text  # take volume
            longName.append(nameStock)
            shortName.append(ticker)
            price.append(priceStock)
            volumn.append(volStock)
    def notiSlack(self,messg):
        slackToken = self.tokenSlack
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        client = scraping.WebClient(slackToken, ssl=ssl_context)
        client.chat_postMessage(
            # channel='@USL3QBUL8',
            channel = self.channel,text=messg)
    def uploadFile(self,nameStock,ticker,priceStock,volStock):
        # upload file
        # save into csv file
        with open('stockprice.csv', 'a') as csv_file:
             writer = csv.writer(csv_file)
             writer.writerow([nameStock,ticker,priceStock,volStock])




