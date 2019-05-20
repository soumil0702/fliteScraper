'''
Created on 19 May 2019

@author: soumi
'''
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


def scrapeResults(driver,city_from, city_to, date_start, date_end,moreResults):
    url=('https://www.kayak.de/flights/' + city_from + '-' + city_to +
             '/' + date_start + '-flexible/' + date_end + '-flexible?sort=price_a')
    driver.get(url)
    print('\n Navigating to url %s \n' % url)
    #sounds_good=driver.find_element_by_xpath('//*[@id="nP60-soundsGood"]')
    #time.sleep(10)
    #Add try-catch block for this shit maybe to handle the ads/popups
    #wait = WebDriverWait(driver, 10)
    
#    time.sleep(10)
    #Try catch for closing the initial popup

    time.sleep(10) 
    try:
        sounds_good='//*[contains(@id,"soundsGood")]'  #try to debug this shite
        myElem = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, sounds_good)))
        driver.find_element_by_xpath(sounds_good).click()  #try to debug this shite
        print('Sounds Good popup found')
    
    except TimeoutException:
        print("Loading.....")
    
    try:
        accept='//*[contains(@id,"accept")]'
        myElem = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, accept)))
        driver.find_element_by_xpath(accept).click()  #try to debug this shite
        print('Accept popup found')
        
    except TimeoutException:
           print("Loading.....")
   
    try:
        driver.find_element_by_xpath('//*[@id="common-icon-x-icon"]/path').click()
        print('Shite popup found')
        
    except :
        print("Loading.....")
        
    try:
        driver.find_element_by_xpath('//div[contains(@class,"visible")]//div//div//*[contains(@id,"dialog-close")]').click()
        print('Email asking popup found')
        
    except:
        print("Loading.....")

    delay =15 # seconds
    loadMore='//a[contains(@id,"loadMore")]'
    '''    try: # Enabling this is not really helping me here for some reason
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, loadMore)))
        print("Page is ready!")
    except TimeoutException:
        print ("Loading took too much time!")
    '''   
    print('..........................Loading Results...... Please Wait a moment..........................')

#    driver.find_element_by_xpath('//a[contains(@id,"loadMore")]').click()
    time.sleep(10)
    driver.find_element_by_xpath(loadMore).click()
    time.sleep(10)
    #sys.exit()
    if(moreResults):
        #I think it would be better if we scroll to the bottom before the two lines below because sometimes its not able to click the more results
        #button for some reason
        print('.......................Loading More Results......................')#execute this if an arg. is supplied
        driver.find_element_by_xpath(loadMore).click()
    
    priceList=[]
    testList=[]
    parsedList=[]
    parsedListTest=[]
    
    # write a jointxpath query: //*[contains(@id,"booking-link") and not (contains(@id,"extra-info"))]
    #//a[contains(@id,"booking-link") and not (contains(@id,"extra-info")) and (contains(@role,"option"))]
    #of main link: //*[@id="d2sD-mb-aE-1ecd230655a-booking-link"]/span[1]
    #of shite link: //*[contains(@id,"extra-info")]/span[1] or //a[contains(@id,"extra-info")]/span[1]#//*[contains(@class,"price option-text") and not (contains(@id,'extra-info'))]
    #priceList=driver.find_elements_by_xpath('//span[contains(@class,"price option-text")]') #This result would give a few
    #more results that aren't too relevant for us
    time.sleep(10)
    print("******************************Extracting Prices*****************************")
    
    priceList=driver.find_elements_by_xpath('//a[contains(@id,"booking-link") and not (contains(@id,"extra-info")) and (contains(@role,"option"))]/span[1]')
    #testList=driver.find_elements_by_xpath('//a[@class="booking-link"]/span[@class="price option-text"]')# this is how the Brazilian dude from Medium does it...same thing really
    #span_elem=driver.find_elements_by_class_name('price option-text')
    
    #r=12;s=23;
    #print('a={:d}, b={:d}'.format(r,s)) #this is how to print a statement
    print('length of priceList ={:d}'.format(len(priceList)))    
    #t=0 #uncomment the below 4 lines to get the print statements of the price list
    #for i in priceList:
    #    print(i.text)
    #    print("Value of span_elem[%d] = %s" % (t,i.text))
    #    t=t+1
    time.sleep(7)
    #driver.quit()
    #testList=[value.text for value in testList ] #another efficient way to fill an array with values
    #print(testList)
    #write if else st. for the case when the currency is in usd!
    parsedList= [price.text.replace('\u20ac','') for price in priceList if price.text != ''] # this command is basically removing euro symbol and getting rid of the blank entries
    parsedList = list(map(int, parsedList)) #converting str to int
    parsedListTest=parsedList
    print('Len(parsedListTest) = %d, Len(parsedList)= %d'%(len(parsedListTest),len(parsedList)))
                
        
    print('Parsed List is :')
    print(parsedList)
    print("Length of PriceList = %d, Length of testList = %d, Length of ParsedList = %d, len of ParsedListTest = %d"%(len(priceList),len(testList),len(parsedList),len(parsedListTest)))
    ##Getting dates now:
    print("******************************Extracting Dates and Days*****************************")
    xp_dates = '//div[@class="section date"]'
    dates = driver.find_elements_by_xpath(xp_dates)
    dates_list = [value.text for value in dates]
    out_date_list = dates_list[::2]
    ret_date_list = dates_list[1::2]
       # Separating the weekday from the day
    out_day = [value.split()[0] for value in out_date_list]
    out_weekday = [value.split()[1] for value in out_date_list]
    ret_day = [value.split()[0] for value in ret_date_list]
    ret_weekday = [value.split()[1] for value in ret_date_list]
    
    print("Out date list is of length %d" % len(out_date_list))
    print(out_date_list)
    
    print("Ret date list is of length %d" % len(ret_date_list))
    print(ret_date_list)
    
    print("Out DAY list is of length %d" % len(out_day))
    print(out_day)
    
    print("Out WEEKDAY list is of length %d" % len(out_weekday))
    print(out_weekday)
    
    print("RET DAY list is of length %d" % len(ret_day))
    print(ret_day)
    
    print("RET WEEKDAY list is of length %d" % len(ret_weekday))
    print(ret_weekday)
    
    #Getting Timings
    print("******************************Extracting Schedules*****************************")
    schedules=[]
    xp_schedule = '//div[@class="section times"]'
    schedules = driver.find_elements_by_xpath(xp_schedule)
    sch_list = [value.text for value in schedules]
    
    hours_list = []
    carrier_list = []
    print("Schedules is of length %d" % len(schedules))
   # print(sch_list)
    for schedule in schedules:
        hours_list.append(schedule.text.split('\n')[0])
        carrier_list.append(schedule.text.split('\n')[1])
    # split the hours and carriers, between a and b legs
    print("hours_list :")
    print(hours_list)
    print("carrier list:")
    print(carrier_list)
    out_hours = hours_list[::2]
    out_carrier = carrier_list[::2]
    ret_hours = hours_list[1::2]
    ret_carrier = carrier_list[1::2]
    print('out_hours :')
    print(out_hours)
    
    print('out_carrier :')
    print(out_carrier)
    
    print('ret_hours :')
    print(ret_hours)
    
    print('ret_carriers :')
    print(ret_carrier)
    
    xp_stops = '//div[@class="section stops"]/div[1]'
    stops = driver.find_elements_by_xpath(xp_stops)
    print('stops length is %d and is :' % len(stops))
    stops_list = [stop.text[0].replace('n','0') for stop in stops]
    stops_list = list(map(int, stops_list)) #converting str to int
    #print('stops_list is: ')
    #print(stops_list)
    out_stop_list = stops_list[::2]
    ret_stop_list = stops_list[1::2]
    return(parsedList,out_day,out_weekday,out_hours,out_stop_list,ret_day,ret_weekday,ret_hours,ret_stop_list,out_carrier,ret_carrier)

