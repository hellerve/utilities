import tempfile
import shutil
import types
import _thread
import threading

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
            return saved[args]
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

@contextmanager
def tempdir():
    outdir = tempfile.mkdtemp()
    try:
        yield outdir
    finally:
        shutil.rmtree(outdir)


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
        clsobj = decorate_cls(clsobj, func=output_name,
                              args=clsname.join(": "))
        return clsobj

@decordecor
def overrides(interface_class):
    """
    Decorator that enables you to make sure that the decorated
    method is really overriding the base classes method you
    want to override.
    """
    def overrider(method):
        assert(method.__name__ in dir(interface_class))
        return method
    return overrider

def synchronized_with_attr(lock_name):
    """Synchronized keyword decorator(see below)
       that is using a premade lock that one can supply."""
    def decorator(method):

        def synced_method(self, *args, **kws):
            lock = getattr(self, lock_name)
            with lock:
                return method(self, *args, **kws)

        return synced_method

    return decorator

def syncronized_with(lock):
    """Decorator factory for the synchronized
       keyword(see below)."""

    def synchronized_obj(obj):

        if type(obj) is types.FunctionType:

            obj.__lock__ = lock

            def func(*args, **kws):
                with lock:
                    obj(*args, **kws)
            return func

        elif isinstance(obj, type):

            orig_init = obj.__init__
            def __init__(self, *args, **kws):
                self.__lock__ = lock
                orig_init(self, *args, **kws)
            obj.__init__ = __init__

            for key in obj.__dict__:
                val = obj.__dict__[key]
                if type(val) is types.FunctionType:
                    decorator = syncronized_with(lock)
                    setattr(obj, key, decorator(val))

            return obj

    return synchronized_obj

def synchronized(item):
    """Adds a synchronized primitive to something,
       similar to the Java keyword."""

    if type(item) is str:
        decorator = synchronized_with_attr(item)
        return decorator(item)

    if type(item) is _thread.LockType:
        decorator = syncronized_with(item)
        return decorator(item)

    else:
        new_lock = threading.Lock()
        decorator = syncronized_with(new_lock)
        return decorator(item)


from opcode import opmap, HAVE_ARGUMENT, EXTENDED_ARG
globals().update(opmap)

def _make_constants(f, builtin_only=False, stoplist=[], verbose=False):
    try:
        co = f.func_code
    except AttributeError:
        return f        # Jython doesn't have a func_code attribute.
    newcode = map(ord, co.co_code)
    newconsts = list(co.co_consts)
    names = co.co_names
    codelen = len(newcode)

    import __builtin__
    env = vars(__builtin__).copy()
    if builtin_only:
        stoplist = dict.fromkeys(stoplist)
        stoplist.update(f.func_globals)
    else:
        env.update(f.func_globals)

    # First pass converts global lookups into constants
    i = 0
    while i < codelen:
        opcode = newcode[i]
        if opcode in (EXTENDED_ARG, STORE_GLOBAL):
            return f    # for simplicity, only optimize common cases
        if opcode == LOAD_GLOBAL:
            oparg = newcode[i+1] + (newcode[i+2] << 8)
            name = co.co_names[oparg]
            if name in env and name not in stoplist:
                value = env[name]
                for pos, v in enumerate(newconsts):
                    if v is value:
                        break
                else:
                    pos = len(newconsts)
                    newconsts.append(value)
                newcode[i] = LOAD_CONST
                newcode[i+1] = pos & 0xFF
                newcode[i+2] = pos >> 8
                if verbose:
                    print(name, '-->', value)
        i += 1
        if opcode >= HAVE_ARGUMENT:
            i += 2

    # Second pass folds tuples of constants and constant attribute lookups
    i = 0
    while i < codelen:

        newtuple = []
        while newcode[i] == LOAD_CONST:
            oparg = newcode[i+1] + (newcode[i+2] << 8)
            newtuple.append(newconsts[oparg])
            i += 3

        opcode = newcode[i]
        if not newtuple:
            i += 1
            if opcode >= HAVE_ARGUMENT:
                i += 2
            continue

        if opcode == LOAD_ATTR:
            obj = newtuple[-1]
            oparg = newcode[i+1] + (newcode[i+2] << 8)
            name = names[oparg]
            try:
                value = getattr(obj, name)
            except AttributeError:
                continue
            deletions = 1

        elif opcode == BUILD_TUPLE:
            oparg = newcode[i+1] + (newcode[i+2] << 8)
            if oparg != len(newtuple):
                continue
            deletions = len(newtuple)
            value = tuple(newtuple)

        else:
            continue

        reljump = deletions * 3
        newcode[i-reljump] = JUMP_FORWARD
        newcode[i-reljump+1] = (reljump-3) & 0xFF
        newcode[i-reljump+2] = (reljump-3) >> 8

        n = len(newconsts)
        newconsts.append(value)
        newcode[i] = LOAD_CONST
        newcode[i+1] = n & 0xFF
        newcode[i+2] = n >> 8
        i += 3
        if verbose:
            print("new folded constant:", value)

    codestr = ''.join(map(chr, newcode))
    codeobj = type(co)(co.co_argcount, co.co_nlocals, co.co_stacksize,
                    co.co_flags, codestr, tuple(newconsts), co.co_names,
                    co.co_varnames, co.co_filename, co.co_name,
                    co.co_firstlineno, co.co_lnotab, co.co_freevars,
                    co.co_cellvars)
    return type(f)(codeobj, f.func_globals, f.func_name, f.func_defaults,
                    f.func_closure)

_make_constants = _make_constants(_make_constants) # optimize thyself!

def bind_all(mc, builtin_only=False, stoplist=[],  verbose=False):
    """Recursively apply constant binding to functions in a module or class.

    Use as the last line of the module (after everything is defined, but
    before test code).  In modules that need modifiable globals, set
    builtin_only to True.

    """
    try:
        d = vars(mc)
    except TypeError:
        return
    for k, v in d.items():
        if type(v) is FunctionType:
            newv = _make_constants(v, builtin_only, stoplist,  verbose)
            setattr(mc, k, newv)
        elif type(v) in (type, ClassType):
            bind_all(v, builtin_only, stoplist, verbose)

@_make_constants
def make_constants(builtin_only=False, stoplist=[], verbose=False):
    """ Return a decorator for optimizing global references.

    Replaces global references with their currently defined values.
    If not defined, the dynamic (runtime) global lookup is left undisturbed.
    If builtin_only is True, then only builtins are optimized.
    Variable names in the stoplist are also left undisturbed.
    Also, folds constant attr lookups and tuples of constants.
    If verbose is True, prints each substitution as is occurs

    """
    if type(builtin_only) == type(make_constants):
        raise ValueError("The bind_constants decorator must have arguments.")
    return lambda f: _make_constants(f, builtin_only, stoplist, verbose)

