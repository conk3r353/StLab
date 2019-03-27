import csv
import json
import typing
import openpyxl


def merge_students_data(csv_file: typing.TextIO, xlsx_workbook: openpyxl.Workbook, json_file: typing.TextIO):
    result = dict()
    sheet = xlsx_workbook['List1']

    csv_data = csv.reader(csv_file)
    csv_list = list(csv_data)

    for row in sheet.iter_rows(values_only=True):
        for line in csv_list:
            if row[0] == ' '.join(line[0:2]):
                result[row[0]] = {'age': int(line[2]), 'marks': [value for value in row[1:] if value]}
    json.dump(result, json_file, indent=0)
