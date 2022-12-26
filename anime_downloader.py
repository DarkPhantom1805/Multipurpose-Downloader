from alive_progress import alive_bar
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
        choose_anime_string = "Search Results:\n"

        for count in range(0, len(tags)):
            choose_anime_string += '\n' + str(count + 1) + '. ' + tags[count].get_text(strip=True)
        
        choose_anime_string += '\n\nChoose an option or Enter -1 to search again: '
        num = int(input(choose_anime_string))
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

Choose an option: """))

            if num == 1:
                start_ep = 0
                end_ep = int(input("\nEnter episode number: "))
            
            elif num == 2:
                start_ep = int(input("\nEnter Starting Episode: "))
                end_ep = int(input("Enter Ending Episode: "))

        else:
            start_ep = end_ep = 1

    id = soup.find(id='movie_id').get('value')
    params = f'?ep_start={start_ep}&ep_end={end_ep}&id={id}'

    return num, params

def get_download_links(mode, params):
    soup = get_html(EPISODE_LIST_URL + params)
    tags =  soup.find_all('a')

    links = []

    if mode == 1:
        soup = get_html(URL + tags[0].get('href').strip())
        link = soup.find('li', {'class' : 'dowloads'}).a.get('href')

        return [link]
    
    if mode == 2:
        for tag in tags:
            path = tag.get('href').strip()
            soup = get_html(URL + path)
            link = soup.find('li', {'class' : 'dowloads'}).a.get('href')
            links.append(link)

        return links

def get_direct_download_links(links):
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
            if not os.path.isfile(path + '\download_page.mhtml'):
                sleep(1)
            else:
                break
        sleep(1)
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
        name = soup.find('span', {'id' : 'title'}).get_text(strip=True).replace(' ', '.')
        
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

        title = {
            'name' : name,
            'links' : links
        }

        return title

    titles = []

    for link in links:
        delete_file()
        open_close(link)
        convert_mhtml_to_html()
        title = get_direct_links()    
        delete_file()
        titles.append(title)

    
    return titles

def choose_quality():
    os.system('cls')
    choose_quality_string = """Available Qualities:

1. 360p
2. 480p
3. 720p
4. 1080p

(If quality is not available, it will be selected automatically)
Select a Quality: """

    return int(input(choose_quality_string))

def download(quality, titles):
    qualities = [360, 480, 720, 1080]
    completed = 0

    curr_dir = os.getcwd() 
    anime_name = " ".join(titles[0].get('name').split(sep='.')[:-2])
    new_path = curr_dir + '\\' + anime_name
    os.mkdir(new_path)

    for title in titles:
        os.system('cls')
        print("Downloading " + title.get('name').replace('.', ' ') + f' ({completed + 1} / {len(titles)})')

        if qualities[quality - 1] != title.get('links')[quality - 1].get('quality'):
            url = title.get('links')[-1].get('link')
        
        url = title.get('links')[quality - 1].get('link')

        x = requests.head(url)
        y = requests.head(x.headers['Location'])

        file_size = int(int(y.headers['content-length']) / 1024)
        chunk_size = 1024

        def compute():
            response = requests.get(url, stream=True)

            with open(new_path + '\\' + title.get('name') + '.mp4', 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
                    yield 1024

        with alive_bar(file_size, bar='classic2', spinner='classic') as bar:
            for i in compute():
                bar()
            
        print(title.get('name').replace('.', ' ') + " Downloaded!")
        completed += 1


if __name__ == "__main__":
    title_path = search()
    (mode, params) = get_episodes(title_path)
    links = get_download_links(mode, params)
    titles = get_direct_download_links(links)
    quality = choose_quality()
    download(quality, titles)