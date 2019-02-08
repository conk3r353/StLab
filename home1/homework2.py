import typing
import functools


def analyze_students(data: typing.Dict) -> typing.Set:
    return {(name, subject, functools.reduce(lambda x, y: x*y, data[name][subject])) for name in data for subject in data[name] if subject != '1C'}


def validate_data(data: typing.Dict) -> bool:
    for name in data:
        if type(name) != str:
            raise TypeError

        for letter in name:
            if ord(letter) > 122 or ord(letter) < 65:
                raise ValueError
            elif ord(letter) in range(91, 97):
                raise ValueError

        for subject in data[name]:
            if type(subject) != str:
                raise TypeError

            for symbol in subject:
                if ord(symbol) not in range(48, 58):
                    if ord(symbol) > 122 or ord(symbol) < 65:
                        raise ValueError
                elif ord(symbol) in range(91, 97):
                    raise ValueError

            for mark in data[name][subject]:
                if type(mark) != int:
                    raise TypeError
                elif mark > 10 or mark < 1:
                    raise ValueError
    return True
