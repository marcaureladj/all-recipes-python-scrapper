from bs4 import BeautifulSoup
import pymysql
import urllib.parse
import urllib.request
import time
import uuid








def liendown(url, pays):

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='boomer',
                                 cursorclass=pymysql.cursors.DictCursor)
                            
    code_food = uuid.uuid4()

    with connection.cursor() as cursor:
        sqlnut = "INSERT INTO `correct_food_types`(`food_code`, `urls`, `types`) VALUES (%s,%s,%s)"
        cursor.execute(sqlnut, (code_food,url,pays))

        connection.commit()

    
connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='boomer',
                                 cursorclass=pymysql.cursors.DictCursor)



sql_select_Query = "SELECT * FROM path_global"
cursor = connection.cursor()
cursor.execute(sql_select_Query)
    # get all records
records = cursor.fetchall()
print("Total number of rows in table: ", cursor.rowcount)

print("\nPrinting each row")

for row in records:
    urls = row["liens"]
    pays = row["types"]
    liendown(urls, pays)
    time.sleep(0.1)



