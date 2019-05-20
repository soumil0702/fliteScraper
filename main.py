#To do: get rid of the additional links of prices that are there.....should be equal to the other entities like number of 
#airline, number of dates,etc. Try getting prices from matrix to see if it is the same as the list from normal method

import sys
import gspread
import pprint
from time import sleep, strftime
from random import randint

from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from symbol import testlist
import scraper as scrape
import spreadsheet as sp
import send_gmail as gmail
from currentPrices import getPriceStats


#sys.stdout = open('out.txt', 'w')

#from tempo import driver  #for some reason if you enable this its also running tempo first and then this script

#Selenium starts here
driver=webdriver.Chrome("C:/Users/soumi/.jenkins/workspace/python_test/flight_scraper_Eclipse/chromedriver.exe")
#driver=webdriver.Chrome() #use this if the chromedriver exists in the Python folder, else use the above line
#driver=webdriver.Firefox()
#driver.set_page_load_timeout(10) #uncomment this na
driver.maximize_window()

moreRes=None#Enable this if you want to extract more results
truncated=True# Disable this if you want many results
#url="https://www.kayak.de/flights/MUC-DEL/2019-05-21-flexible/2019-05-24-flexible?sort=price_a"
cityFrom="MUC"
cityTo="DEL"
dateStart="2019-05-28"
dateEnd="2019-06-07"
url=('https://www.kayak.de/flights/' + cityFrom + '-' + cityTo +
             '/' + dateStart + '-flexible/' + dateEnd + '-flexible?sort=price_a')
old_lowest,old_avg=getPriceStats()

print('Initial lowest_price that was saved in Spreadsheet= %f and Initial avg. = %f'% (old_lowest,old_avg))

prices,out_day,out_weekday,out_hours,out_stop_list,ret_day,ret_weekday,ret_hours,ret_stop_list,out_carrier,ret_carrier=scrape.scrapeResults(driver,
                                                                                                                                            cityFrom,
                                                                                                                                            cityTo,
                                                                                                                                            dateStart,
                                                                                                                                            dateEnd,
                                                                                                                                            moreRes)
print('@@@@@@@@@@@@@@@@@@@@@@ Scraped what I could scrape, closing WebDriver @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
sp.clearPrices()
time.sleep(4)
driver.quit()

oldTS,newTS=sp.spreadSheet(prices, 
                           out_day, 
                           out_weekday, 
                           out_hours,
                           out_stop_list,
                           ret_day,
                           ret_weekday,
                           ret_hours, 
                           ret_stop_list,
                           out_carrier,
                           ret_carrier,
                           truncated)
time.sleep(4)
new_lowest,new_avg=getPriceStats()
print('Latest lowest_price = %d and Final avg. = %f'% (new_lowest,new_avg))
print('\n***********************Results successfully saved in Spreadsheet*******************************')

#Here i send an email only if the lowesr price is < 0.80*status quo
if  new_lowest<old_lowest:
    print('\n*****************************Lower Prices found !!!!!!!! ...........Sending mail to recipeint******************\n')   
    recipients=["soumil.bharatendu@gmail.com"]
    subject="Prices dropped in Kayak!!! (auto. gen. from Python, Se)"
    body="See spreadsheet flitscraper on GSheets \n \n Previous Lowest Price @ TimeStamp - %s : %f , Previous avg. price\
    : %f \n \n New Lowest Price @ TimeStamp - %s : %f, New avg. Price: %f\n For booking goto: %s" % (oldTS,old_lowest,old_avg,newTS,new_lowest,new_avg,url)
    gmail.send_email_two('soumil.bharatendu@gmail.com', 'Bhole789!!',recipients, subject, body)


