from fileinput import filename
import logging
import os
from datetime import datetime
from csv import writer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
dir_path = os.path.dirname(os.path.realpath(__file__))
file_name = os.path.join(dir_path,'complaints_log.log')
csv_file_name = os.path.join(dir_path,'complaints.csv')

# print(file_name)
print(csv_file_name)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(filename=file_name)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')  # Last I checked this was necessary.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()

try:
    logging.info('Logging into EMIS')  
    driver.get("http://emis.ubteb.go.ug:8080/")
    time.sleep(5)
    driver.find_element(by=By.CSS_SELECTOR, value='#user_login').send_keys('frank@ubteb.go.ug')
    time.sleep
    driver.find_element(by=By.CSS_SELECTOR, value='#user_password').send_keys('frank2020')
    time.sleep(2)
    driver.find_element(by=By.CSS_SELECTOR, value='input[data-disable-with="Log in"]').click()
    time.sleep(15)
    logger.info('loading complaints page')
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
    
    with open(csv_file_name, 'a') as csv_file:
        csv_writer = writer(csv_file)
        csv_writer.writerow(list)
        csv_file.close()
    logger.info('Pending Complaints: %s In Progress Complaints: %s Complete Complaints: %s', pending, in_progress, complete)
except Exception as err:
    logger.warning('failed operation \n\n\n\n', err)
    #//TODO send message incase of failure