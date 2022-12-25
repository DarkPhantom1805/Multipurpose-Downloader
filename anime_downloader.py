from bs4 import BeautifulSoup

import requests
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

        num = int(input('\n\nChoose an option or Enter -1 to search again: '))
        if num != -1: break

    return tags[num-1].a.get('href')
        
def get_episodes(path):
    soup = get_html(URL + path)
    type = soup.find('p', {'class' : 'type'}).get_text(strip=True)

    if 'movie' in type.lower():
        start_ep = 1
        end_ep = 0

    else:
        episodes = 1

        tags = soup.findAll(id="episode_page")
        for child in tags[0].descendants:
            if child.name == 'a':
                num_eps = int(child.get('ep_end'))
                if num_eps > episodes:
                    episodes = num_eps

        clear_screen()
        print(f'Found {str(episodes)} episodes!')
        
        if episodes > 1:
            num = int(input("""
1. Download Single Episode
2. Download Multiple Episodes

Select One: """))

            if num == 1:
                start_ep = 0
                end_ep = int(input("Enter episode number: "))
            
            elif num == 2:
                start_ep = int(input("\nEnter Starting Episode: "))
                end_ep = int(input("\nEnter Ending Episode: "))

        else:
            start_ep = end_ep = 1

    id = soup.find(id='movie_id').get('value')
    f'?ep_start={start_ep}&ep_end={end_ep}&id={id}'

if __name__ == "__main__":
    title_path = search()
    get_episodes(title_path)