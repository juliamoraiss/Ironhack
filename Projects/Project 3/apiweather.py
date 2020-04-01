#!/usr/bin/env python
# coding: utf-8

# # Importando Libraries


import requests
import datetime
import pandas as pd
import sqlalchemy as db


pd.set_option('display.max_columns', None)


# # Api hgbrasil

url = 'https://api.hgbrasil.com/weather?woeid=455827'
response = requests.get(url)
info = response.json()


# ## Tempraturas máxima e mínima do dia

temp_min = info['results']['forecast'][0]['min']
temp_max = info['results']['forecast'][0]['max']


# # Criação de dataframe

df = pd.DataFrame()

def insert_values():
    df['Data'] = datetime.date.today()
    df['Cidade'] = pd.Series(['São Paulo'])
    df['Temperatura Mínima'] = temp_min
    df['Temperatura Máxima'] = temp_max


insert_values()

df = pd.concat([insert_values(), df], ignore_index=True)

# # Atualizando Tabela de Temperatura

def update_table(title, df):
    engine = db.create_engine('postgresql://postgres:admin@localhost/farmacia_tempo')
    conn = engine.connect()
    df.to_sql(title, con=conn, if_exists='append', index = False)
    conn.close()


update_table('temperatura', df)

print('oi')

