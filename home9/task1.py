import requests
from lxml import html
from threading import Thread
import datetime


URL = 'https://www.countryflags.io/'
NAMES_XPATH = '//*[@id="countries"]/div/div/div/p[2]/text()'
LINKS_XPATH = '//*[@id="countries"]/div/div/div/img/@src'


def get_links():
    site = requests.get(URL)
    tree = html.fromstring(site.content)

    names = tree.xpath(NAMES_XPATH)
    links = tree.xpath(LINKS_XPATH)
    result = dict(zip(names, links))
    return result


class DownloadThread(Thread):
    def __init__(self, name, link):
        super().__init__()
        self.name = name
        self.link = link

    def run(self):
        with open(f'flags/{self.name}.png', 'wb') as pic:
            pic_request = requests.get(URL+self.link)
            pic.write(pic_request.content)


def linear_download():
    start = datetime.datetime.now()

    for flag in get_links().items():
        with open(f'flags_linear/{flag[0]}.png', 'wb') as pic:
            pic_request = requests.get(URL + flag[1])
            pic.write(pic_request.content)

    print(f'Без потоков: {datetime.datetime.now() - start}')


def create_threads():
    start = datetime.datetime.now()

    for flag in get_links().items():
        thread = DownloadThread(flag[0], flag[1])
        thread.start()

    print(f'C потоками: {datetime.datetime.now() - start}')


create_threads()
linear_download()
