import requests
from lxml import html
import datetime
import asyncio
import aiohttp


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


async def download_pic(flag):
    async with aiohttp.ClientSession() as session:
        response = await session.get(URL+flag[1])
        data = await response.read()
        with open(f'flags_async/{flag[0]}.png', "wb") as f:
            f.write(data)
        return data


futures = [download_pic(flag) for flag in get_links().items()]

start = datetime.datetime.now()

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(futures))

print(f'C async потоками: {datetime.datetime.now() - start}')
