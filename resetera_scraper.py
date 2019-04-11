import requests
import time
from jinja2 import Environment, select_autoescape
from tqdm import trange
from bs4 import BeautifulSoup

DOMAIN = "https://www.resetera.com"
BASE_URL = DOMAIN + "/forums/video-games.7/page-{}"
HEADERS = {
    'User-Agent': 'ResetERA user minimaxir',
}
MAX_PAGES = 2

env = Environment()

template_str = """~~~{{ title }}~~~

{% for post in posts[:20] -%}
{{ post['data-author'] }}: {{ post.div.article.text | trim }}
-----
{% endfor %}
!~END~!
"""

template = env.from_string(template_str)


def process_thread(thread_url, template):
    req = requests.get(thread_url, headers=HEADERS)
    soup = BeautifulSoup(req.text, features="html5lib")

    # Remove special embeds
    bbcodes = soup.find_all("div", {"class": "bbCodeBlock"})
    for bbcode in bbcodes:
        bbcode.decompose()

    title = soup.find("h1", {"class": "p-title-value"}).text
    if 'OT' in title:
        return None
    posts = soup.find_all("article", {"class": "message"})

    text = template.render(title=title, posts=posts)
    return text

with open('resetera_videogames.txt', 'w') as f:
    for page in trange(1, MAX_PAGES+1):
        url = BASE_URL.format(page)
        req = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(req.text, features="html5lib")
        thread_urls = [DOMAIN + x.a['href'] for x in soup.find_all(
            "div", {"class": "structItem-title"})]
        for thread_url in thread_urls:
            thread = process_thread(thread_url, template)
            if thread is not None:
                f.write(thread + "\n")
        time.sleep(1)  # to avoid overloading server
