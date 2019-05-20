'''
Created on 19 May 2019

@author: soumi
'''
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

def getPriceStats():
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<Getting current Prices from Spreadsheet>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    scope= ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds=ServiceAccountCredentials.from_json_keyfile_name('client_secret.json',scope)
    client=gspread.authorize(creds)
    sheet=client.open('flitescraper').sheet1
    CurrentAvg=sheet.col_values(11)
    
    parsedCurrAvg=[]
    for i in range(0,len(CurrentAvg)-1):parsedCurrAvg.append(CurrentAvg[i+1])
    parsedCurrAvg = list(map(int, parsedCurrAvg)) #converting str to int
    print(parsedCurrAvg)
    try:
        avg=sum(parsedCurrAvg)/len(parsedCurrAvg)
        print('length of price entries from spreadsheet = %d'%len(parsedCurrAvg))
        print('Current avg. costs are : %f'% avg)
        lowestPrice=parsedCurrAvg[0]
        print("Lowest price is %d"%lowestPrice)
        
        return lowestPrice,avg
    except:
        print("Error division by 0 !!! in avg. computation")
        return 0,0
 
   