import requests
import time
from tqdm import trange
from bs4 import BeautifulSoup

BASE_URL = "https://www.resetera.com/forums/video-games.7/page-{}"
HEADERS = {
    'User-Agent': 'ResetERA user minimaxir',
}

max_pages = 1164

with open('resetera_videogames.txt', 'w') as f:
    for page in trange(1, max_pages):
        url = BASE_URL.format(page)
        req = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(req.text, features="html5lib")
        titles = [x.a.text for x in soup.find_all(
            "div", {"class": "structItem-title"})]
        for title in titles:
            f.write(title + "\n")
        time.sleep(1)  # to avoid overloading server
