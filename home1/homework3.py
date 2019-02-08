class FibIterator:
    def __init__(self):
        self.a = 0
        self.b = 1
        self.count = 0

    def __iter__(self):
        while True:
            yield self.a
            self.a, self.b = self.b, self.a + self.b
            self.count += 1
            if self.count == 100:
                break


def fib_generator():
    a, b = 0, 1
    for i in range(100):
        yield a
        a, b = b, a + b


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
