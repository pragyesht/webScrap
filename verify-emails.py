import mysql.connector
from datetime import date
import random
from validate_email import validate_email

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


def get_url(my_table):
    cursor = mysql_connect()
    # cursor.execute("SELECT id, email FROM "+my_table+" WHERE status = 3 AND id = 18;")
    cursor.execute("SELECT id, email FROM "+my_table+" WHERE status = 3 "
                   " ORDER BY `id` ASC LIMIT " + str(random.randrange(0, 2)) + ", 1;")
    # print(cursor.statement)
    results = cursor.fetchone()
    cursor.close()
    mysql_commit_close()
    return results


def update_url(my_table, url_id, email_validation):
    cursor = mysql_connect()
    sql_update = "UPDATE "+my_table+" SET `is_email_valid` = %s, `status` = '4' WHERE `id`=%s "
    ins_data = (int(email_validation), str(url_id))
    cursor.execute(sql_update, ins_data)
    print(url_id)
    cursor.close()
    mysql_commit_close()
    return True


table = 'cbse_school_org'
data = get_url(table)

while data:
    if data[1]:
        isvalid = validate_email(data[1])
    else:
        isvalid = bool(0)

    update_url(table, data[0], isvalid)

    data = get_url(table)
