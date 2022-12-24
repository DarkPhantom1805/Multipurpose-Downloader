import requests, m3u8
from bs4 import BeautifulSoup
from requests_html import HTMLSession
SESSION = HTMLSession()

NAME = input("\nEnter the name of the Anime: ").lower()
# TYPE = input("Enter one. 'Sub' or 'Dub': ").lower()

URL = 'https://gogoanime.bid'
SEARCH_PATH = '/search.html?keyword='
EPISODE_LIST_URL = 'https://ajax.gogo-load.com/ajax/load-list-episode'

keyword = NAME.strip().replace(' ', '%20')

def getStreamLinks(id) -> list:
    headers = {
        'authority': 'gogohd.pro',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'referer': 'https://gogoanime.bid/',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'iframe',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }

    params = {
        'id': id,
    }

    response = requests.get('https://gogohd.pro/streaming.php', params=params, headers=headers)
    links = []

    soup = BeautifulSoup(response.content, 'html.parser')
    tags = soup.find_all('li', {'class' : 'linkserver'})
    for tag in tags:
        links.append(tag.get('data-video'))

    print(links)
    return links[1]

r = requests.get(URL + SEARCH_PATH + keyword)
soup = BeautifulSoup(r.content, 'html.parser')

tags = soup.find_all('p', {'class'    : 'name'})
found = False
dub = False

confirmation = input('\nIs "'+ tags[0].get_text(strip=True) +'" the title you are searching for? Y/N: ').lower()

if confirmation == 'y': 
    found = True
    TITLE_PATH = tags[0].a.get('href')

r = requests.get(URL + TITLE_PATH)
soup = BeautifulSoup(r.content, 'html.parser')

TOTAL_EPISODES = 0

tags = soup.findAll(id="episode_page")
for child in tags[0].descendants:
    if child.name == 'a':
        num_eps = int(child.get('ep_end'))
        if num_eps > TOTAL_EPISODES:
            TOTAL_EPISODES = num_eps

single = False
confirmation = input('Do you want to download a single episode? Y/N: ').lower()
if confirmation == 'y': single = True

if single:
    start_ep = int(input("Enter Episode Number: "))
    end_ep = start_ep
else:
    start_ep = int(input("Enter Starting Episode Number: "))
    end_ep = int(input("Enter Ending Episode Number: "))

anime_id = soup.find(id='movie_id').get('value')
EPISODE_LIST_PARAMS = f'?ep_start={start_ep}&ep_end={end_ep}&id={anime_id}'

r = requests.get(EPISODE_LIST_URL + EPISODE_LIST_PARAMS)
soup = BeautifulSoup(r.content, 'html.parser')
tags =  soup.find_all('a')

EPISODE_PATHS = []

for child in tags:
    EPISODE_PATHS.append(child.get('href').strip())

for path in EPISODE_PATHS:
    r = requests.get(URL + path)
    soup = BeautifulSoup(r.content, 'html.parser')
    episode_id = soup.find('li', {'class' : 'dowloads'}).a.get('href').split(sep='=')[1].split(sep='&')[0]
    
    download_link = getStreamLinks(episode_id)
