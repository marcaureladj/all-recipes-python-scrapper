import requests
from bs4 import BeautifulSoup
import os
import pymysql
import random
import urllib.parse
import urllib.request

def imagedown(url, folder):

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='boomer',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
    except:
        pass
    os.chdir(os.path.join(os.getcwd(), folder))

    req = urllib.request.Request(url)
    req.add_header('Cookie', 'euConsent=true')
    html_content = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html_content, 'html.parser')
    namescode = random.randint(0, 1000)
	
    ingredients = soup.findAll("li", {"class": "ingredients-item"})
    nutritivesname = soup.findAll("span", {"class": "nutrient-name"})
    imgdiv = soup.find("div", {"class": "image-container"})
    images = imgdiv.findAll("img", src=True)

    steps = soup.findAll("li", {"class": "subcontainer instructions-section-item"})
    name = soup.find("h1", {"class": "headline heading-content elementFont__display"}).get_text().replace("®", "")

    direction_data = soup.find("section", {"class": "recipe-meta-container two-subcol-content clearfix recipeMeta"})
    prep_time = direction_data.find("div", {"class": "recipe-meta-item"}).get_text()
    cook_time = direction_data.find("div", {"class": "recipe-meta-item"}).get_text()
    total_time = direction_data.find("div", {"class": "recipe-meta-item"}).get_text()

    description = soup.find("div", {"class": "recipe-summary elementFont__dek--within"})
    paragraph = description.find("p", {"class": "margin-0-auto"}).get_text()

    namescode = random.randint(0, 1000000)
    id_code = namescode

    with connection.cursor() as cursor:
        sqlprep = "INSERT INTO `infos`(`id_code`, `cook_time`, `prep_time`, `total_time`) VALUES (%s,%s,%s,%s)"
        cursor.execute(sqlprep, (id_code, cook_time, prep_time, total_time))

        connection.commit()

    for namenutri in nutritivesname :
        str_nutri = namenutri.find("span", {"class": "elementFont__details--bold elementFont__transformCapitalize"}).get_text()
        str_value = namenutri.find("span", {"class": "nutrient-value"}).get_text()
        if str_nutri and str_value:
            with connection.cursor() as cursor:
                sqlnutri = "INSERT INTO `food_nutritive`(`id_code`, `nutrives`, `vals`) VALUES (%s,%s,%s)"
                cursor.execute(sqlnutri, (id_code, str_nutri, str_value))

                connection.commit()


    for ingredient in ingredients:
        str_ing = ingredient.find("span", {"class": "checkbox-list-checkmark"}).get_text()
        if str_ing and str_ing != "Add all ingredients to list":
            
            with connection.cursor() as cursor:
                sqling = "INSERT INTO `food_ingredients`(`id_code`, `ingredients`) VALUES (%s,%s)"
                cursor.execute(sqling, (id_code, str_ing))

                connection.commit()


    for step in steps:
        str_step = step.get_text()
        if str_step:
           
            with connection.cursor() as cursor:
                sqlstep = "INSERT INTO `food_step`(`id_code`, `steps`) VALUES (%s,%s)"
                cursor.execute(sqlstep, (id_code,  str_step))

                connection.commit()





    with connection.cursor() as cursor:
        sqls = "INSERT INTO `images`(`id_code`, `food_names`, `food_descript`) VALUES (%s,%s,%s)"
        cursor.execute(sqls, (id_code, name, paragraph))

        connection.commit()

 
        
            # select src tag
        image_src = [x['src'] for x in images]
            # select only jp format images
        image_src = [x for x in image_src if x.endswith('.jpg')]
        image_count = 1
        for image in image_src:
            names = '_'+str(image_count)+'.jpg'
            with open('Breakfast-Burritos_image_'+str(image_count)+'.jpg', 'wb') as f:
                res = requests.get(image)
                f.write(res.content)
            image_count = image_count+1

            
            with connection.cursor() as cursor:
                sqls = "INSERT INTO `images_bank`(`id_code`, `img_link`, `paths`) VALUES (%s,%s,%s)"
                cursor.execute(sqls, (id_code, names, folder))

                connection.commit()





imagedown('https://www.allrecipes.com/recipe/244796/labneh-lebanese-yogurt/', 'Breakfast-Burritos')