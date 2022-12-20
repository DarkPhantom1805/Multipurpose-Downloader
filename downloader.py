import requests
from bs4 import BeautifulSoup

# THIS PROJECT IS JUST TO SCRAPE ZORO.TO AND DOWNLOAD ANIME USING IT

# Make a request and get the return the HTML content of a webpage
def getWebpage(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, 'html.parser') 

# Search the title and get it's Page Url
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

# Get the direct download links from the Web page
def getNumberofEpisodes(watchUrl):
    episodes = 0

    # Send a request to the Anime's page on the website
    try:
        soup = getWebpage(watchUrl)
        # print(soup.prettify())

    except Exception as e:
        print(f"Unexpected Error {e}. Please try again!")
        return None

    episodeData = soup.find_all(id='episode_page')
    
    # Extract the number of episodes 
    for tag in episodeData:
        for a in tag.find_all('a'):
            for number in a.get_text().split(sep='-'):
                if int(number) >= episodes: episodes = int(number)

    return episodes

def downloadEpisode(number, url):
    episodePath = url.split(sep='/')
    url = f'https://gogoanime.bid/{episodePath[-1]}-episode-{number}'

    try:
        soup = getWebpage(url)
    except Exception as e:
        print(e)
        return None

    downloadUrl = soup.find_all('li', {'class' : 'downloads'})
    print(downloadUrl)


# Main function of the program
def main():
    animeName = input("Enter Anime Name: ").lower()
    animeUrl = getAnimeUrl(animeName)
    if animeUrl is not None: episodes = getNumberofEpisodes(animeUrl)
    episodeToDownload = input(f"\nEnter Episode number to download: (0 - {episodes}): ")
    downloadEpisode(episodeToDownload, animeUrl)

if __name__ == "__main__":
    main()