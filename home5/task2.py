import requests
import re


def get_weather():
    url = 'https://yandex.by/pogoda/'
    city_regex = r"<a.*?place-list__item-name.*?/pogoda/([a-z-]+).*?>([А-яё -]+)</a>"
    weather_regex = r'(?<=<span class="temp__value">)([+−]\d)(?=</span>)'
    result = dict()

    data = requests.get(url+'region/149')
    cities = re.findall(city_regex, data.text, re.MULTILINE)

    for city in cities:
        city_info = requests.get(url+city[0])
        city_weather = re.search(weather_regex, city_info.text).group()
        if '−' in city_weather:
            city_weather = -1 * int(city_weather[1::])
        elif '+' in city_weather:
            city_weather = int(city_weather[1::])
        else:
            city_weather = int(city_weather)
        result[city[1]] = city_weather
    return result


print(get_weather())
