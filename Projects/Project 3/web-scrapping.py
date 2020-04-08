#!/usr/bin/env python
# coding: utf-8

# # Importando Bibliotecas


import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import datetime
import sqlalchemy as db


# # Mostrando todas as linhas


pd.set_option('display.max_rows', None)


# # Lista de Remédios Populares para Gripe


lst_med = ['ibuprofeno', 'dipirona', 'paracetamol', 'diclofenaco', 'nimesulida']


# # Extraindo informações da Drogasil


def create_df_preco(med):
    url = f'https://busca.drogasil.com.br/search?w={med}&cnt=100'
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'lxml')
    df_remedio_preco = pd.DataFrame()
    
        
    lst_price = []
    lst_ean = []
    
    produtos = soup.find_all('li', {'class': 'products-card-v2__item-card'})
    produtos = [produto for produto in produtos]
        
    lst_url_produto = [item.find_all('a')[1]['title'] for item in produtos]

    for url_produto in lst_url_produto:
        response = requests.get(url_produto)
        html = response.content
        soup = BeautifulSoup(html)
        price = soup.find_all('span', {'class':'price'})[-1].text.strip().replace('R$\n', '').replace('R$','').replace(',','.')
        lst_price.append(float(price))
        
    for i in range(len(lst_url_produto)):
        url = lst_url_produto[i]
        mini_df_drogasil = pd.read_html(url, index_col=0)[-2]
        try:
            ean = mini_df_drogasil.loc['EAN',1]
            lst_ean.append(int(ean))
        except:
            pass

    df_remedio_preco['EAN'] = lst_ean
    df_remedio_preco['Preço'] = lst_price
    df_remedio_preco['Data'] = datetime.date.today()

    return df_remedio_preco


# # Criando DataFrames

dfs_preco = []

for med in lst_med:
    df_remedio_preco = create_df_preco(med)
    dfs_preco.append(df_remedio_preco)



df_remedio_preco = pd.concat(dfs_preco)



df_remedio_preco


# # Atualizando Database

def update_table(title, df):
    engine = db.create_engine('postgresql://postgres:admin@localhost/farmacia_tempo')
    conn = engine.connect()
    df.to_sql(title, con=conn, if_exists='append', index = False)
    conn.close()


update_table('ean_preco', df_remedio_preco)
