from flask import Flask, render_template, request
import requests
import json


def get_rates():
    currencies = dict()
    for item in requests.get('http://www.nbrb.by/API/ExRates/Currencies').json():
        abbreviation = item['Cur_Abbreviation']
        name = item['Cur_Name']
        currencies[abbreviation] = name
        with open('rates.json', 'w') as rates:
            json.dump(currencies, rates, indent=4, ensure_ascii=False)


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    amount = ''
    result = ''
    currency = ''
    reverse = 0
    with open('rates.json') as rates:
        items = json.load(rates)
        if request.method == 'POST':
            amount = request.form.get('amount')
            currency = request.form.get('currency')
            if request.form.get('action') == 'update':
                get_rates()
                return render_template('index.html',
                                       data=items,
                                       result=result,
                                       amount=amount,
                                       currency=currency,
                                       reverse=reverse)
            item = requests.get(f'http://www.nbrb.by/API/ExRates/Rates/{currency}?ParamMode=2').json()
            scale = item['Cur_Scale']
            rate = item['Cur_OfficialRate']
            if request.form.get('action') == 'convert':
                result = round(int(amount) / float(rate) * int(scale), 2)
            elif request.form.get('action') == 'convert-reverse':
                reverse = 1
                result = round(int(amount) * float(rate) / int(scale), 2)

        return render_template('index.html',
                               data=items,
                               result=result,
                               amount=amount,
                               currency=currency,
                               reverse=reverse)


if __name__ == '__main__':
	get_rates()
    app.run()
