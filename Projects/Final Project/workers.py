def href(page):
    import requests
    from bs4 import BeautifulSoup
    url = f'https://www.tudogostoso.com.br/receitas?page={page + 1}'
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)
    receitas_href = ['https://www.tudogostoso.com.br' +
                     href.a['href'] for href in soup.find_all('div', 'card recipe-card recipe-card-with-hover')]
    return receitas_href


def create_recipe(href):
    import requests
    from bs4 import BeautifulSoup
    import sqlalchemy as db
    import pandas as pd
    import re

    try:
        response = requests.get(href)
        if response.status_code == 200:
            html = response.content
            soup = BeautifulSoup(html)
            name = soup.find_all('div', {'class': 'recipe-title'})[0].h1.text.replace('\n', '')
            prep_time = (soup.find_all('time', {'class': 'dt-duration'})[0].text.replace('\n', ''))
            portion = soup.data.text.replace('\n', '')
            cat = soup.find_all('span', {'property': 'name'})[1].text.replace('\n', '')
            prep_mode = soup.find_all('div', {'class': 'instructions e-instructions'})[0].find_all('p')
            if len(prep_mode) == 0:
                prep_mode = soup.find_all('div', {'class': 'instructions e-instructions'})[0].find_all('span')
            prep = ''
            for elem in prep_mode:
                elem = elem.text
                prep += ' ' + elem
            prep = prep.replace('"', "")

            ingredients = [ingredient.text.replace('\xa0', '') for ingredient in
                      soup.find_all('span', {'class': 'p-ingredient'})]

            engine = db.create_engine(f'{DATABASE_URL}')
            conn = engine.connect()
            query = f"INSERT INTO recipes.recipes_df VALUES (null, %s, %s, %s, %s, %s, %s, %s)"
            engine.execute(query, (name, prep_time, portion, href, prep, cat, str(ingredients)))
            conn.close()
    except:
        pass

    return ''



def get_images(href):
    import requests
    import pandas as pd
    from bs4 import BeautifulSoup
    import sqlalchemy as db

    try:
        response = requests.get(href)
        if response.status_code == 200:
            html = response.content
            soup = BeautifulSoup(html)
            src_img = soup.find_all('img', {'itemprop': 'image'})[0]
            img_source = src_img['src']

            engine = db.create_engine(f'{DATABASE_URL}')
            conn = engine.connect()
            query = f"INSERT INTO recipes.images VALUES (null, %s, %s)"
            engine.execute(query, (img_source, href))
            conn.close()

    except:
        pass

    return ''

def get_images(href):
    import requests
    from bs4 import BeautifulSoup
    import sqlalchemy as db

    response = requests.get(href)
    if response.status_code == 200:
        html = response.content
        soup = BeautifulSoup(html)
        src_img = soup.find_all('img', {'itemprop': 'image'})
        if len(src_img) > 0:
            src_img = src_img[0]
            img_source = src_img['src'].split('?')[0]
            engine = db.create_engine(f'{DATABASE_URL}')
            conn = engine.connect()
            query = f"INSERT INTO recipes.images VALUES (null, %s, %s)"
            engine.execute(query, (img_source, href))
            conn.close()


    return ''
