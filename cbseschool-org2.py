import time
from selenium import webdriver
import re
import mysql.connector
from datetime import date
import random
import urllib.parse
import requests
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


def get_url_wefunder():
    cursor = mysql_connect()
    # cursor.execute("SELECT id, url FROM cbse_school_org WHERE status = 1 AND id = 18;")
    cursor.execute("SELECT id, url FROM cbse_school_org WHERE status = 1 "
                   " ORDER BY `cbse_school_org`.`id` ASC LIMIT " + str(random.randrange(0, 2)) + ", 1;")
    # print(cursor.statement)
    results = cursor.fetchone()
    cursor.close()
    mysql_commit_close()
    return results


def working_url(url_id):
    cursor = mysql_connect()
    cursor.execute(
        "UPDATE `cbse_school_org` SET `status` = '2' WHERE `cbse_school_org`.`id` = '" + str(url_id) + "';")
    print(cursor.statement)
    cursor.close()
    mysql_commit_close()
    return True


def update_url(url_id, school_name1, affiliate, address1, pin, std, office, res, my_email,
               foundation_year, principals_name, schools_level, society_name):
    cursor = mysql_connect()
    sql_update = "UPDATE `cbse_school_org` SET `school_name`=%s, affiliate_id=%s, address=%s, pin_code=%s, " \
                 "std_code=%s, office_phone=%s, res_phone=%s, email=%s, found_year=%s, principal_name=%s, " \
                 "school_level=%s, society=%s, `status` = '3'  WHERE `cbse_school_org`.`id`=%s "
    ins_data = (school_name1, affiliate, address1, pin, std, office, res,
                my_email, foundation_year, principals_name, schools_level, society_name, str(url_id))
    cursor.execute(sql_update, ins_data)
    print(url_id)
    cursor.close()
    mysql_commit_close()
    return True


url = get_url_wefunder()
table = 'cbse_school_org'

option = webdriver.ChromeOptions()
option.add_argument('--headless')
# option.add_argument("--window-size=1920,23500")
# option.add_argument('--no-sandbox')
# option.add_argument('--disable-dev-sh-usage')


while len(url[1]) > 9:
    working_url(url[0])
    response = requests.get(urllib.parse.unquote(url[1]))

    if response.status_code != 404:
        driver = webdriver.Chrome('drivers\chromedriver.exe', options=option)

        driver.get(urllib.parse.unquote(url[1]))
        # driver.maximize_window()
        driver.minimize_window()

        school_name = affiliate_id = address = pin_code = std_code = office_phone = res_phone = email = found_year = \
            principal_name = school_level = society = ''
        elements = driver.find_elements_by_xpath('//*[@id="responsivetable"]/table/tbody/tr')
        for row in elements:
            fields = row.find_elements_by_css_selector('td')
            i = 0
            head = value = ''
            for val in fields:
                i += 1
                if i == 1:
                    head = val.text
                elif i == 2:
                    value = val.text

                # print(head, value)

                if head == 'Name':
                    school_name = value
                elif head == 'Affiliate ID':
                    affiliate_id = value
                elif head == 'Address':
                    address = value
                elif head == 'PIN Code':
                    pin_code = value
                elif head == 'STD Code':
                    std_code = value
                elif head == 'Office Phone':
                    office_phone = value
                elif head == 'Residence Phone':
                    res_phone = value
                elif head == 'E-mail':
                    email = value
                elif head == 'Foundation Year':
                    found_year = value
                elif head == 'Principal/Head of Institution':
                    principal_name = value
                elif head == 'School Status':
                    school_level = value
                elif head == 'Managing Trust/Society/Committee':
                    society = value

        # print('school_name-', school_name)
        # print('affiliate_id-', affiliate_id)
        # print('address-', address)
        # print('pin_code-', pin_code)
        # print('std_code-', std_code)
        # print('office_phone-', office_phone)
        # print('res_phone-', res_phone)
        # print('email-', email)
        # print('found_year-', found_year)
        # print('principal_name-', principal_name)
        # print('school_level-', school_level)
        # print('society-', society)

        #
        update_url(url[0], school_name, affiliate_id, address, pin_code, std_code, office_phone, res_phone, email,
                   found_year, principal_name, school_level, society)
        #
        # # time.sleep(1)
        driver.quit()

    # break
    url = get_url_wefunder()
