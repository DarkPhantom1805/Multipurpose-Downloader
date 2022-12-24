import requests
from bs4 import BeautifulSoup

EPISODE_LIST_URL = 'https://ajax.gogo-load.com/ajax/load-list-episode'
EPISODE_LIST_PARAMS = f'?ep_start=1&ep_end=2&id=625'

URL = 'https://gogoanime.bid/dragon-ball-z-episode-1'

# r = requests.get(EPISODE_LIST_URL + EPISODE_LIST_PARAMS)
# soup = BeautifulSoup(r.content, 'html.parser')

# tags =  soup.find_all('a')

# episode_paths = []

# for child in tags:
    # episode_paths.append(child.get('href').strip())

r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html.parser')
print(soup.find('li', {'class' : 'dowloads'}).a.get('href').split(sep='=')[1])
