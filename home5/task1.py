import requests


def get_exchange_rate(currency: str) -> float:
    url = 'http://www.nbrb.by/API/ExRates/Rates/'

    data = requests.get(url+f'{currency}?ParamMode=2')

    if data.status_code != 200:
        raise SystemExit(f'Error code: {data.status_code}')

    scale = data.json()['Cur_Scale']
    rate = data.json()['Cur_OfficialRate']

    return round(rate/scale, 2)
