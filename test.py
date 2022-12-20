from bs4 import BeautifulSoup
import requests

def getWebpage(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, 'html.parser') 

def getAnimeUrl(titleName):

    # Turn Anime name into Url path
    keyword = titleName.replace(' ', '%20')
    SearchURL = f'https://gogoanime.bid/search.html?keyword={keyword}'

    # Get the HTML contents of the website and seperate the useful content (Anime title and Links) 
    try:    
        soup = getWebpage(SearchURL)
        titles = soup.findAll('p', {'class' : 'name'},  limit=None)

    except Exception as e:
        print(e)
        return None

    # Search the content for Anime title and extract it's link
    try:
        title = soup.find('p', {'class' : 'name'})
        confirmation = input(f'\nIs this the Title you were searching for?: \n{title.get_text(strip=True)} \nY/N: ').lower()

        if confirmation == 'y':
            path = title.a.get('href')
            watchURL = f'https://gogoanime.bid{path}'
            return watchURL

        else:
            for title in titles:
                for content in title:
                    if titleName in content.get('title').lower():
                        path = content.get('href')
                        watchURL = f'https://gogoanime.bid{path}'
                        return watchURL

                    continue
    except:
        pass
    
    print("Couldn't Find title. Check spellings and please try again!")
    return None

animeName = input("Enter Anime Name: ").lower()
animeUrl = getAnimeUrl(animeName)
print(animeUrl)