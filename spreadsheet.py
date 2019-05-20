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

def spreadSheet(prices,out_day,out_weekday,out_hours,out_stops,ret_day,ret_weekday,ret_hours,ret_stops,out_carrier,ret_carrier,truncated):
    print('\n \n<<<<<<<<<<<<<<<<<<<<<<<<<<<<Saving Results to Spreadsheet>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
    scope= ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds=ServiceAccountCredentials.from_json_keyfile_name('client_secret.json',scope)
    client=gspread.authorize(creds)
    sheet=client.open('flitescraper').sheet1
    #pp=pprint.PrettyPrinter()
    #result=sheet.get_all_records();
    #pp.pprint(result)
    
    #result=sheet.row_values(4) #comment this its only for printing row contents of row 3
    #result=sheet.col_values(3)
    #sheet.update_cell(7,10,3)
    #result=(sheet.cell(7,10).value)+'Jheezy'
    
    #to add your own row:
    oldTS=sheet.cell(2,12).value

    #sheet.insert_row(row,index)
    #sheet.delete_row(3)
    
    sheet.update_cell(2,12,strftime("Start: %H:%M - %d-%m-%Y" ))
    limit=0
    if truncated: limit=15 #this would basically limit the records
    for i in range(0,len(prices)-limit):
        sheet.update_cell(i+2,1,out_day[i])
        time.sleep(1)
        sheet.update_cell(i+2,2,out_weekday[i])
        time.sleep(0.5)
        sheet.update_cell(i+2,3,out_hours[i])
        time.sleep(1)
        sheet.update_cell(i+2,4,out_stops[i])
        time.sleep(0.5)
        sheet.update_cell(i+2,5,ret_day[i])
        time.sleep(1)    
        sheet.update_cell(i+2,6,ret_weekday[i])
        time.sleep(0.5)
        sheet.update_cell(i+2,7,ret_hours[i])
        time.sleep(1)
        sheet.update_cell(i+2,8,ret_stops[i])
        time.sleep(0.5)
        sheet.update_cell(i+2,9,out_carrier[i])
        time.sleep(1)
        sheet.update_cell(i+2,10,ret_carrier[i])
        print('..................Please wait............. \n')
        time.sleep(0.5)
        print('................')
        sheet.update_cell(i+2,11,prices[i])
        time.sleep(1.5)#change this to 2 or 2.5 if it doesnt work
        print('..Spreadsheet is being populated with extracted results ............\n')

    newTS=sheet.cell(2,12).value
    sheet.update_cell((len(prices)-limit)+1,12,strftime("End: %H:%M - %d-%m-%Y" ))
    return oldTS,newTS
#    sheet.update_cell(,2)-----
def clearPrices():
    print('\n \n<<<<<<<<<<<<<<<<<<<<<<<<<<<<Clearing up the old Prices column in Spreadsheet>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
    scope= ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds=ServiceAccountCredentials.from_json_keyfile_name('client_secret.json',scope)
    client=gspread.authorize(creds)
    sheet=client.open('flitescraper').sheet1
    CurrentAvg=sheet.col_values(11)
    for i in range(1,len(CurrentAvg)):
        sheet.update_cell(i+1,11,'')
        time.sleep(1)
    
