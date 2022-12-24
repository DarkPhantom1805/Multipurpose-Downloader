import requests
from bs4 import BeautifulSoup
import m3u8
from alive_progress import alive_bar


# url = 'https://wwwx18.gofcdn.com/videos/hls/u_1HTbWGUrqwoAvIZxDaEA/1671764760/193557/14a369cc45ca9c73d70872708160af7d/'
# m3u8_file = 'ep.1.1665506470.360.m3u8'

# r = requests.get(url + m3u8_file)
# m3u8_master = m3u8.loads(r.text)
# segments = m3u8_master.data['segments']
# for segment in segments:
#     print(segment)
# with open('video.mp4', 'wb') as f:
#     for segment in segments:
#         uri = segment['uri']
#         r = requests.get(url + uri)
#         f.write(r.content)
