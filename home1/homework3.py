class FibIterator:
    def __init__(self):
        self.digit_1 = 0
        self.digit_2 = 1
        self.count = 0

    def __iter__(self):
        while True:
            yield self.digit_1
            self.digit_1, self.digit_2 = self.digit_2, self.digit_1 + self.digit_2
            self.count += 1
            if self.count == 100:
                break


def fib_generator():
    digit_1, digit_2 = 0, 1
    for count in range(100):
        yield digit_1
        digit_1, digit_2 = digit_2, digit_1 + digit_2


def strange_decorator(func):
    def count_args(*args, **kwargs):
        if len(args) + len(kwargs) > 10:
            raise ValueError
        for kwarg in kwargs:
            if type(kwargs[kwarg]) == bool:
                raise TypeError
        if type(func(*args, **kwargs)) == int:
            return func(*args, **kwargs) + 13
        return func(*args, **kwargs)
    return count_args
