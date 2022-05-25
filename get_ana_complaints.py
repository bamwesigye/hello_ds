import logging
from datetime import datetime
import time, logging
from csv import writer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')  # Last I checked this was necessary.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()
try:
    print('Logging into EMIS')  
    driver.get("http://emis.ubteb.go.ug:8080/")
    time.sleep(5)
    driver.find_element(by=By.CSS_SELECTOR, value='#user_login').send_keys('frank@ubteb.go.ug')
    time.sleep
    driver.find_element(by=By.CSS_SELECTOR, value='#user_password').send_keys('frank2020')
    time.sleep(2)
    driver.find_element(by=By.CSS_SELECTOR, value='input[data-disable-with="Log in"]').click()
    time.sleep(15)
    print('loading complaints page')
    driver.get ('http://emis.ubteb.go.ug:8080/complains')
    time.sleep(20)
    driver.find_element(by=By.CSS_SELECTOR, value='#filterrific_with_complain_status').send_keys('Pending')
    time.sleep(20)
    pending = driver.find_element(by=By.CSS_SELECTOR, value='#results > div.well > div:nth-child(2)').text.split(' ')[6]

    driver.find_element(by=By.CSS_SELECTOR, value='#filterrific_with_complain_status').send_keys('in progress')
    time.sleep(20)
    in_progress = driver.find_element(by=By.CSS_SELECTOR, value='#results > div.well > div:nth-child(2)').text.split(' ')[6]

    driver.find_element(by=By.CSS_SELECTOR, value='#filterrific_with_complain_status').send_keys('complete')
    time.sleep(20)
    complete = driver.find_element(by=By.CSS_SELECTOR, value='#results > div.well > div:nth-child(2)').text.split(' ')[6]
    day = datetime.now().strftime('%d/%m/%Y %H:%S')
    cur_week = datetime.now().strftime('%W')
    list= [cur_week,day,pending,in_progress,complete]
    with open('anacomplaints.csv', 'a') as csv_file:
        csv_writer = writer(csv_file)
        csv_writer.writerow(list)
        csv_file.close()
    print(datetime.now().strftime("%Y %m %d %H:%M"),"Task completed Succesfully")
    
except Exception as err:
    print('failed operation \n\n\n\n', err)
    #//TODO send message incase of failure