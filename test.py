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

titles = [{'name' : 'Boku no hero academia season 3 episode 1'}]
anime_name = " ".join(titles[0].get('name').split(sep=' ')[:-2:])

print(anime_name)