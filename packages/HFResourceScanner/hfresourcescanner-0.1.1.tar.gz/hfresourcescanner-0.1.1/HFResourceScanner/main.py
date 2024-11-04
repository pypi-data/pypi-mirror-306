def a():
    print("a")
def b():
    print("b")
def c():
    print("c")

funcs = {"a": a, "b": b, "c": c}

# v1
"""
for f, func in funcs.items():
    if f == "a":
        def nf(*args):
            print("New a")
            return func(*args)
        a = nf
    elif f == "b":
        def nf(*args):
            print("New b")
            return func(*args)
        b = nf
    elif f == "c":
        def nf(*args):
            print("New c")
            return func(*args)
        c = nf
"""

# v2
def nf(*args):
    print("New a")
    func = funcs["a"]
    return func(*args)
a = nf

def nf(*args):
    print("New b")
    func = funcs["b"]
    return func(*args)
b = nf

def nf(*args):
    print("New c")
    func = funcs["c"]
    return func(*args)
c = nf


a()
b()
c()
