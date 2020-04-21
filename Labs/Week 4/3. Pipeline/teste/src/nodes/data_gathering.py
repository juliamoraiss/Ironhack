import logging
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

logger = logging.getLogger('nodes.data_gathering')


def update(client, params):

	response = requests.get(params.url)
	soup = BeautifulSoup(response.content)

	movie_names = [movie.find('a')['title'].replace('Filme ', '') for movie in
				   soup.find_all('div', attrs={'class': 'col-sm-6 col-md-3'})]
	movie_links = ['https://www.cinemark.com.br/' + movie.find('a')['href'] for movie in
				   soup.find_all('div', attrs={'class': 'col-sm-6 col-md-3'})]

def done(client, params):
	pass