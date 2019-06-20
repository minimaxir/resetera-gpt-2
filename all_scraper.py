import requests
import time
import re
import csv
from tqdm import trange
from bs4 import BeautifulSoup


FORUMS = ['gaming-forum.7', 'etcetera-forum.9']
DOMAIN = "https://www.resetera.com"
BASE_URL = DOMAIN + "/forums/{}/page-{}"
HEADERS = {
    'User-Agent': 'ResetERA user minimaxir',
}
MAX_PAGES = 1400

with open('resetera_all.csv', 'w') as f:
    w = csv.writer(f)
    w.writerow(['forum', 'thread_title'])
    for forum in FORUMS:
        forum_name = forum.split('-')[0]
        for page in trange(1, MAX_PAGES+1):
            url = BASE_URL.format(forum, page)
            req = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(req.text, features="html5lib")
            thread_texts = [x.a.text for x in soup.find_all(
                "div", {"class": "structItem-title"})]
            for text in thread_texts:
                if text is not None and "|OT" not in text:
                    w.writerow([forum_name, text])
            time.sleep(1)  # to avoid overloading server
