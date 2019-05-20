import gspread
import pprint
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Selenium starts here
def temp():
    driver=webdriver.Chrome() #use this if the chromedriver exists in the Python folder, else use the above line
    driver.set_page_load_timeout(10)
    driver.get("http://google.com")
    driver.find_element_by_xpath('//*[@id="gb_70"]').click()
    #driver.find_element_by_name("btnK").send_keys(Keys.ENTER)
    #sounds_good=driver.find_element_by_xpath('//*[@id="nP60-soundsGood"]')
    #time.sleep(10)
    wait = WebDriverWait(driver, 10)
    
    driver.quit()
    