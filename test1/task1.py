class Logger(type):

    def __new__(mcs, clsname, bases, dct):
        mod_class = super().__new__(mcs, clsname, bases, dct)
        mod_class.LogItem = collections.namedtuple('LogItem', 'name args kwargs result')

        def func_call(self, func):
            def catch(*args, **kwargs):
                self.log.append(self.LogItem(func.__name__, [args], {kwargs}, func(*args, **kwargs)))
                return func(*args, **kwargs)
            return catch

        for name, value in dct.items():
            if not name.startswith('__'):
                if isinstance(value, types.FunctionType):
                    setattr(mod_class, name, func_call(value))
        return mod_class


class B(metaclass=Logger):
    def __init__(self):
        self.log = []

    @property
    def last_log(self):
        return self.log[-1:-4:-1]

    def say_hi(self):
        return 'Hi'
