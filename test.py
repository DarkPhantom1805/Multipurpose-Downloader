# import libraries
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# specify the url
urlpage = 'https://gogoanime.bid/chainsaw-man-episode-1' 

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

driver.get(urlpage)

soup = BeautifulSoup(driver.page_source)
print(soup.prettify())
driver.close()
