import json
import openpyxl
import typing


def xlsx_to_json(xlsx_workbook, json_file: typing.TextIO):
    sheet = xlsx_workbook["List"]
    result = dict()
    key_1 = ''
    for row in sheet.iter_rows():
        if row[0].value is not None:
            if result.get(row[0].value) is None:
                key_1 = row[0].value
                result[key_1] = dict()
        result[key_1][row[1].value] = row[2].value
    json.dump(result, json_file, indent=0)


with open('test_json.json', 'w') as test_json:
    wb = openpyxl.load_workbook('test_xlsx.xlsx')
    xlsx_to_json(wb, test_json)
