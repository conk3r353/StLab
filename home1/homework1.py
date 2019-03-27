import typing
import decimal
import fractions
import collections


def get_max_and_min(data: typing.Set[typing.Union[decimal.Decimal, fractions.Fraction, str]]) -> typing.NamedTuple[
            typing.Union[decimal.Decimal, fractions.Fraction]]:
    for element in data:
        if isinstance(element, str):
            try:
                str_num = decimal.Decimal(element)
                data.discard(element)
                data.add(str_num)
            except decimal.InvalidOperation:
                digit_1 = ''
                for i in element:
                    if i.isdigit():
                        digit_1 += i
                    else:
                        break
                digit_2 = element[len(digit_1)+3:len(element)+1]
                data.discard(element)
                data.add(fractions.Fraction(int(digit_1), int(digit_2)))
    Result = collections.namedtuple('Result', 'max_value min_value')
    result = Result(max(data), min(data))
    return result
