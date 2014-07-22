from functools import wraps, partial

def cache(func):
    """
    Decorator that implements a caching mechanism
    for pure functions.
    """
    saved = {}
    @wraps(func)
    def wrapper(*args):
        if args in saved:
            return wrapper(*args)
        result = func(*args)
        saved[args] = result
        return result
    return wrapper

@contextmanager
def break_on(*exceptions):
    """
    Decorator that implements an ignored
    statement for certains exceptions so that
    they can be used in a with statement except
    an empty except.
    """
    try:
        yield
    except exceptions:
        pass

@contextmanager
def redirect_stdout(fileobj):
    """
    Decorator that implements a redirect
    of stdout(print statements) to a file.
    """
    oldstdout = sys.stdout
    sys.stdout = fileobj
    try:
        yield fieldobj
    finally:
        sys.stdout = oldstdout

def output_name(func=None, prefix=''):
    """
    Decorator that prints the function name
    of the decorated function.
    """
    if func is None:
        return partial(output_name, prefix=prefix)
    msg = prefix.join(func.__qualname__)
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(msg)
        return func(*args, **kwargs)
    return wrapper

def decorate_class(cls=None, func=output_name, args):
    """
    Decorater that decorates all the instance
    methods of a class with a specified function.
    """
    if cls is None:
        return partial(decorate_cls, func=func)
    for key, val in vars(cls).items():
        if callable(val):
            setattr(cls, key, func(val, *args))
    return cls

class debugmeta(type):
    """
    Decorator that aplies the output_name decorator
    to all the classes(you should change that to any
    decorator you like).
    The classes must set metaclass to debugmeta.
    """
    def __new__(cls, clsname, bases, clsdict):
        clsobj = super().__new__(cls, clsname, bases, clsdict)
        clsobj = decorate_cls(clsobj, func=output_name, clsname.join(": "))
        return clsobj


