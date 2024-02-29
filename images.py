from bs4 import BeautifulSoup
import pymysql
import urllib.parse
import urllib.request
import time

def liendown(url, pays):

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='boomer',
                                 cursorclass=pymysql.cursors.DictCursor)
                            




    req = urllib.request.Request(url)
    req.add_header('Cookie', 'euConsent=true')
    html_content = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html_content, 'html.parser')
    
    
    

    li = soup.find("ul", {"class": "carouselNav__list elementFont__resetList recipeCarousel__list"})
    
    if li:
        carrous = li.findAll("a", {"class": "carouselNav__link recipeCarousel__link"}, href=True)
        liens_src = [x['href'] for x in carrous]
                    # select only jp format images
        neliens_src = [x for x in liens_src]
        for nliens in  neliens_src:
                if nliens and nliens !="#":
                    with connection.cursor() as cursor:
                        sqlnutri = "INSERT INTO `spaths`(`liens`, `types`) VALUES (%s,%s)"
                        cursor.execute(sqlnutri, (nliens, pays))

                        connection.commit()
    
   








connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='boomer',
                                 cursorclass=pymysql.cursors.DictCursor)



sql_select_Query = "SELECT * FROM `souspaths`"
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




