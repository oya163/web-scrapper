#!python3

'''
    Scraps the webpage with login
    Checks the particular time of latest post
    If that's the latest post in this particular hour
    Then send email notification

    Prepare exe using pyinstaller as follows:-
    1. pyinstaller scrapper.py --onefile
    2. Modify scrapper.spec to include emailSender.py
    3. pyinstaller scrapper.spec
    4. scrapper.exe is inside dist/
'''

import requests
import datetime
import urllib3
from bs4 import BeautifulSoup
from selenium import webdriver
import emailSender as postman
import argparse
import sys

# parser = argparse.ArgumentParser(description='Email Sender Parser')
# parser.add_argument('path', metavar='PATH', help='path to store secret file')
#
# args = parser.parse_args()

if __name__ == '__main__':
    with requests.Session() as session:
        driver = webdriver.PhantomJS()

        # This URL will be the URL that your login form points to with the "action" tag.
        postURL = 'https://my3.my.umbc.edu/login'

        # This URL is the page you actually want to pull down with requests.
        requestURL = 'https://my3.my.umbc.edu/groups/classifieds'

        payload = {
            'username-input-name': 'EMAIL-ADDRESS', 'password-input-name': 'PASSWORD'
        }

        http = urllib3.PoolManager()
        post = session.post(postURL, data=payload)
        driver.get(requestURL)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        for updates in soup.find_all("div", class_="today update-day"):
            t = updates.find("span", class_="time").text
            curr_date = datetime.datetime.now()
            latest_time = datetime.datetime.strptime(t," %I:%M %p")
            final_time = latest_time.replace(year=curr_date.year, month=curr_date.month, day=curr_date.day)
            if final_time.hour == curr_date.hour:
                print("Sending messages for latest update @ ", final_time)
                postman.StartMessage()
        driver.quit()
    sys.exit()