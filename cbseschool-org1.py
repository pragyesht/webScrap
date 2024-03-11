import time
from selenium import webdriver
import re
import mysql.connector
from datetime import date

import urllib.parse
from selenium.webdriver.chrome.options import Options

today = date.today()
cnx = ''


def mysql_connect():
    global cnx
    cnx = mysql.connector.connect(
        user='root', password='', host='127.0.0.1', database='6steps')
    return cnx.cursor(buffered=True)


def mysql_commit_close():
    global cnx
    cnx.commit()
    cnx.close()


def ins_url_wefunder(url, locate):
    cursor = mysql_connect()
    parse_url = urllib.parse.quote(url)
    cursor.execute("SELECT id, url FROM cbse_school_org WHERE url = '" + parse_url + "';")
    row_count = cursor.rowcount

    if row_count == 0:
        add_url = ("INSERT INTO cbse_school_org (url, location, status) "
                   "VALUES (%s, %s, %s)")
        data_url = (urllib.parse.quote(url), locate, 1)
        cursor.execute(add_url, data_url)

    # ins_id = cursor.lastrowid
    cursor.close()
    mysql_commit_close()
    # return ins_id


locations = ['andaman-nicobar', 'andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar', 'chandigarh', 'chattisgarh',
             'dadar-nagar-haveli', 'daman-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh',
             'jammu-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
             'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
             'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal']

option = webdriver.ChromeOptions()
# option.add_argument('--headless')
# option.add_argument("--window-size=1920,23500")
# option.add_argument('--no-sandbox')
# option.add_argument('--disable-dev-sh-usage')

for location in locations:
    page = 1
    while page != 0:
        url = 'https://www.cbseschool.org/location/' + location + '/page/' + str(page) + '/'
        driver = webdriver.Chrome('drivers\chromedriver.exe', options=option)

        driver.get(urllib.parse.unquote(url))
        driver.maximize_window()
        driver.minimize_window()

        rows = driver.find_elements_by_class_name('catbox')
        for row in rows:
            href = row.find_element_by_css_selector('h2').find_element_by_css_selector('a').get_attribute('href')
            print(href)
            ins_url_wefunder(href, location)
            # time.sleep(1)

        next_links = driver.find_elements_by_class_name('nextpostslink')
        if next_links:
            page += 1
        else:
            page = 0

        driver.quit()
