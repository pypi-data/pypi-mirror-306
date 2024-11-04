
def wraponce(fun):
    original = fun
    name = fun.__name__
    def temp(*args, **kwargs):
        print("Wrapped function working!")
        result = fun(*args, **kwargs)
        globals()[name] = original
        return result*2
    globals()[name] = temp

def timeonce(fun, scanner):
    original = fun
    name = fun.__name__
    def temp(*args, **kwargs):
        s = time.time()
        result = fun(*args, **kwargs)
        e = time.time()
        globals()[name] = original
        return result*2
    globals()[name] = temp


def add(a, b):
    return a + b

def calc():
    x = 10
    y = 20

    z = add(x, y)

    print(z)

calc()
wraponce(add)
calc()
calc()
