import requests, m3u8
from bs4 import BeautifulSoup
import webbrowser
import pyautogui as pag
from time import sleep
import os
import shutil
from io import BytesIO
import quopri
import time
from alive_progress import alive_bar

URL = 'https://gogoanime.bid'
SEARCH_PATH = '/search.html?keyword='
EPISODE_LIST_URL = 'https://ajax.gogo-load.com/ajax/load-list-episode'

def get_direct_download_links(URL):
    path = os.getcwd() + '\html'

    def open_close(url):
        os.makedirs(path)

        webbrowser.open(url)
        sleep(4)
        pag.hotkey('ctrl', 's')
        sleep(1)
        pag.typewrite('download_page.mhtml')
        pag.press('tab', presses=6, interval=0.1)
        pag.press('enter')
        pag.typewrite(path)
        pag.press('enter', presses=4, interval=0.1)
        while not os.path.exists(path + '\download_page.mhtml'):
            time.sleep(1)

            if not os.path.isfile(path + '\download_page.mhtml'):
               time.sleep(1)
            else:
                break

        pag.hotkey('ctrl', 'w')
        pag.hotkey('alt', 'tab')


    def delete_file():
        shutil.rmtree(path, ignore_errors=True)

    def convert_mhtml_to_html():

        with open('html\download_page.mhtml', 'r', encoding='utf8') as f:
            content = f.read()
            inputFile = BytesIO((content).encode('utf-8'))
            outputFile = BytesIO()

            quopri.decode(inputFile, outputFile)

        os.rename(path + '\download_page.mhtml', path + '\download_page.html')

        with open("html\download_page.html", "wb") as f:
            f.write(outputFile.getbuffer())        
    
    def get_direct_links():
        links = []
        try:
            with open('html\download_page.html', 'r', encoding='utf8') as f:
                soup = BeautifulSoup(f, 'html.parser')
        except:
            with open('html\download_page.html', 'r', encoding='latin-1') as f:
                soup = BeautifulSoup(f, 'html.parser')

        tags = soup.find_all('a', {'download' : ''})

        for tag in tags:
            if '360' in tag.get_text(strip=True).lower():
                links.append({
                    'link' : tag.get('href'),
                    'quality' : '360'
            })
            elif '480' in tag.get_text(strip=True).lower():
                links.append({
                    'link' : tag.get('href'),
                    'quality' : 480
            })
            elif '720' in tag.get_text(strip=True).lower():
                links.append({
                    'link' : tag.get('href'),
                    'quality' : 720
            })
            elif '1080' in tag.get_text(strip=True).lower():
                links.append({
                    'link' : tag.get('href'),
                    'quality' : 1080
            })
        
        return links

    delete_file()
    open_close(URL)
    convert_mhtml_to_html()
    links = get_direct_links()    
    delete_file()
    return links

while True:
    NAME = input("\nEnter the name of the Anime: ").lower()
    keyword = NAME.strip().replace(' ', '%20')

    r = requests.get(URL + SEARCH_PATH + keyword)
    soup = BeautifulSoup(r.content, 'html.parser')

    tags = soup.find_all('p', {'class'    : 'name'})

    choose_anime_string = """
Search Results:"""

    for count in range(0, len(tags)):
        choose_anime_string += '\n' + str(count + 1) + '. ' + tags[count].get_text(strip=True)

    choose_anime_string += '\nSelect One or Enter -1 to search again: '
    num = int(input(choose_anime_string))

    if num != -1: break

TITLE_PATH = tags[num-1].a.get('href')

r = requests.get(URL + TITLE_PATH)
soup = BeautifulSoup(r.content, 'html.parser')

type = soup.find('p', {'class' : 'type'}).get_text(strip=True)

if 'movie' in type.lower():
    start_ep = 1
    end_ep = 0

else:

    TOTAL_EPISODES = 0

    tags = soup.findAll(id="episode_page")
    for child in tags[0].descendants:
        if child.name == 'a':
            num_eps = int(child.get('ep_end'))
            if num_eps > TOTAL_EPISODES:
                TOTAL_EPISODES = num_eps

    start_ep = int(input(f"Enter Episode Number (1 - {str(TOTAL_EPISODES)}) : "))
    end_ep = start_ep

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
    link = soup.find('li', {'class' : 'dowloads'}).a.get('href')
    
direct_links = get_direct_download_links(link)

def choose_quality(links):
    choose_quality_string = """
Available Qualities:"""

    for count in range(0, len(links)):
        choose_quality_string += '\n' + str(count + 1) + '. ' + str(links[count].get('quality')) + 'p'

    choose_quality_string += '\nSelect One: '
    return int(input(choose_quality_string))

quality = choose_quality(direct_links)

def download(quality, links):
    URL = links[quality - 1].get('link')

    x = requests.head(URL)
    y = requests.head(x.headers['Location'])

    file_size = int(int(y.headers['content-length']) / 1024)
    chunk_size = 1024

    def compute():
        response = requests.get(URL, stream=True)
        with open('video.mp4', 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                yield 1024

    with alive_bar(file_size, bar='classic2', spinner='classic') as bar:
        for i in compute():
            bar()

download(quality, direct_links)