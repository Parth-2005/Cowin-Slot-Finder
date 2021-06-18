from selenium import webdriver
from datetime import datetime
import requests
import time
import json

with open('user_info.json', 'r') as c:
    user_info = json.load(c)["user_info"]


dist = user_info['district code']

# driver.find_element_by_xpath("//button[5]").click()
# date = datetime.now().strftime("%d-%m-%Y")
date = '18-06-2021'
URL = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}'.format(
    dist, date)

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}


def findAvailability():
    counter = 0
    result = requests.get(URL, headers=header)
    response_json = result.json()
    data = response_json["sessions"]
    for each in data:
        if((each["available_capacity"] > 0) & (each["min_age_limit"] == 18)&(each["available_capacity_dose1"]>0)&(each["fee_type"] == 'Free')):
            counter += 1
            print(each)
            print(each["name"])
            print(each["pincode"])
            print(each["vaccine"])
            print(each["available_capacity"])
            print(each["available_capacity_dose1"])
            print(each["available_capacity_dose2"])
            return True
    if(counter == 0):
        print("No Available Slots")
        return False


while findAvailability() != True:
    findAvailability()

driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://selfregistration.cowin.gov.in/")
time.sleep(2)
driver.find_element_by_id("mat-input-0").send_keys(str(user_info['phone number']))
time.sleep(2)
driver.find_element_by_class_name('login-btn').click()