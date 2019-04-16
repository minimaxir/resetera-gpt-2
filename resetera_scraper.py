import requests
import time
import re
from jinja2 import Environment, select_autoescape
from tqdm import trange
from bs4 import BeautifulSoup

DOMAIN = "https://www.resetera.com"
BASE_URL = DOMAIN + "/forums/video-games.7/page-{}"
HEADERS = {
    'User-Agent': 'ResetERA user minimaxir',
}
MAX_PAGES = 1000

# https://stackoverflow.com/a/12825283
def regex_replace(s, find, replace):
    return re.sub(find, replace, s)


env = Environment()
env.filters['regex_replace'] = regex_replace

template_str = """~!~{{ title }}

{% for post in posts[:10] -%}
{% if post.div.article.text | regex_replace('\n\n+', '\n') | length > 4 %}{{ post['data-author'] }}: {{ post.div.article.text[:2000] | regex_replace('https?://\S+', '') | regex_replace('\n\n+', '\n') | trim }}
-----{% endif %}
{% endfor %}<|endoftext|>
"""

template = env.from_string(template_str)


def process_thread(thread_url, template):
    req = requests.get(thread_url, headers=HEADERS)
    soup = BeautifulSoup(req.text, features="html5lib")

    # Remove special embeds
    bbcodes = soup.find_all("div", {"class": "bbCodeBlock"})
    for bbcode in bbcodes:
        bbcode.decompose()

    try:
        title = soup.find("h1", {"class": "p-title-value"}).text
        if '|' in title:
            return None
        posts = soup.find_all("article", {"class": "message"})
        text = template.render(title=title, posts=posts)
    except:
        return None
    return text

with open('resetera_videogames_1000.txt', 'w') as f:
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
