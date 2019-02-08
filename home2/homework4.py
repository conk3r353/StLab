import types


class Pep8Warrior(type):
    def __new__(mcs, clsname, bases, dct):
        new_attrs = {}
        for name, val in dct.items():
            if not name.startswith('__'):
                if isinstance(val, types.FunctionType):
                    new_attrs[name.lower()] = val
                elif isinstance(val, type):
                    name_list = [sym for sym in name.title()]
                    i = name_list.count('_')
                    for underscore in range(i):
                        pos = name_list.index('_')
                        name_list[pos + 1] = name_list[pos + 1].upper()
                        name_list.pop(pos)
                    new_attrs[''.join(name_list)] = val
                else:
                    new_attrs[name.upper()] = val
        return type.__new__(mcs, clsname, bases, new_attrs)


def pep8_warrior(clsname, bases, dct):
    new_attrs = {}
    for name, val in dct.items():
        if not name.startswith('__'):
            if isinstance(val, types.FunctionType):
                new_attrs[name.lower()] = val
            elif isinstance(val, type):
                name_list = [sym for sym in name.title()]
                while name_list[len(name_list)-1] == '_':
                    name_list.pop(len(name_list)-1)
                i = name_list.count('_')
                for underscore in range(i):
                    pos = name_list.index('_')
                    name_list[pos + 1] = name_list[pos + 1].upper()
                    name_list.pop(pos)
                new_attrs[''.join(name_list)] = val
            else:
                new_attrs[name.upper()] = val
    return type(clsname, bases, new_attrs)
