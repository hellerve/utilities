from datetime import datetime
from functools import wraps, partial
from contextlib import contextmanager

def decordecor(decorator):
    """
    Decorator that can be used to turn simple functions
    into well-behaved decorators as long as the decorators
    are fairly simple. If a decorator expects a function and
    returns a function (no descriptors), and if it doesn't
    modify function attributes or docstring, then it is
    eligible to use this. Simply apply @decordecor to
    your decorator and it will automatically preserve the
    docstring and function attributes of functions to which
    it is applied.
    """
    def new_decorator(f):
        g = decorator(f)
        g.__name__ = f.__name__
        g.__doc__ = f.__doc__
        g.__dict__.update(f.__dict__)
        return g
    new_decorator.__name__ = decorator.__name__
    new_decorator.__doc__ = decorator.__doc__
    new_decorator.__dict__.update(decorator.__dict__)
    return new_decorator

@decordecor
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

@decordecor
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

@decordecor
def timefun(func):
    @wraps(func)
    def new_func(*args, **kwargs):
        before = datetime.utcnow()
        func(*args, **kwargs)
        after = datetime.utcnow()
        print("{0} function took {1} seconds.".format(func, after - before))
    return new_func

@decordecor
def decorate_class(cls=None, func=output_name, args=None):
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
        clsobj = decorate_cls(clsobj, func=output_name, args=clsname.join(": "))
        return clsobj


