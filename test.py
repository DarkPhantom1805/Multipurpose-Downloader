from bs4 import BeautifulSoup
from time import sleep
from io import BytesIO

import pyautogui as pag
import webbrowser
import requests
import shutil
import quopri
import sys
import os

URL = 'https://gogoanime.bid'
SEARCH_PATH = '/search.html?keyword='
EPISODE_LIST_URL = 'https://ajax.gogo-load.com/ajax/load-list-episode'

def clear_screen():
    os.system('cls')

def get_html(url):
    try:
        r = requests.get(url)
        return BeautifulSoup(r.content, 'html.parser')

    except Exception as e:
        print(e)
        sys.exit()

def search():
    while True:
        clear_screen()
        keyword = input("Search for Anime: ").lower().strip().replace(' ', '%20')

        soup = get_html(URL + SEARCH_PATH + keyword)
        tags = soup.find_all('p', {'class'    : 'name'})

        if not tags:
            print("Couldn't find the title you were searching for! Try again later.")
            sys.exit()

        clear_screen()
        choose_anime_string = "Search Results:"

        for count in range(0, len(tags)):
            choose_anime_string += '\n' + str(count + 1) + '. ' + tags[count].get_text(strip=True)
        
        choose_anime_string += '\nChoose an option or Enter -1 to search again: '
        num = int(input(choose_anime_string))
        if num != -1: break

    return tags[num-1].a.get('href')

search()