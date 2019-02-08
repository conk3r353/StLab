import typing
import re


class RegParser:
    ADDRESS_REGEX = r'^(?:[A-Z][A-Za-z]*, )?(?:[A-Z][a-z]*(?: [Cc]ity)?, )?(?:[A-Za-z \-_0-9]+(?: str\.)?),' \
                    r' (?:\d+ *[\-/\\,|] *\d+)$'
    CONTACT_REGEX = r'^(?:(?:name=(?P<name>[-\w ]*)|surname=(?P<surname>[-\w ]*)|age=(?P<age>[-\w ]*)|' \
                    r'city=(?P<city>[-\w ]*))(?:;|$)){1,4}(?<!;)$'
    PRICE_REGEX = r'(?<=[\$€] )\d+(?:[.,]?\d+)|\d+(?:[.,]?\d+)(?= *BYN)'

    @classmethod
    def find(cls, data: str, choice: int) -> typing.List[typing.Union[typing.Dict, str, int, float]]:
        result = []
        if choice == 1:
            result = re.findall(cls.ADDRESS_REGEX, data, re.MULTILINE)
        elif choice == 2:
            for match in re.finditer(cls.CONTACT_REGEX, data, re.MULTILINE):
                iter_dict = {key: value for key, value in match.groupdict().items() if value}
                result.append(iter_dict)
        elif choice == 3:
            regex = re.findall(cls.PRICE_REGEX, data, re.MULTILINE)
            for item in regex:
                if '.' in item:
                    result.append(float(item))
                elif ',' in item:
                    result.append(float(item.replace(',', '.')))
                else:
                    result.append(int(item))
        return result
