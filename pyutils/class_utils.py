from decorators import _make_constants

class Closer:
    '''A context manager to automatically close an object with a close method
    in a with statement.'''

    def __init__(self, obj):
        self.obj = obj

    def __enter__(self):
        return self.obj

    def __exit__(self, exception_type, exception_val, trace):
        try:
           self.obj.close()
        except AttributeError:
           pass

class LookupOptimizingMetaclass(type):
    '''A metaclass that uses the _make_constants function to optimize
       out repeated function lookups.'''
    def __init__(cls, name, bases, dict):
        super(OptimizingMetaclass, cls).__init__(name, bases, dict)

        import types
        for name, attribute in dict.items():
            if type(attribute) is types.FunctionType:
                dict[name] = _make_constants(attribute)

def build_optimizing_metaclass(builtin_only=False, stoplist=[], verbose=False):
    '''Factory function that builds a configurable optimizing metaclass.'''
    from types import FunctionType
    class _OptimizingMetaclass(type):
        def __init__(cls, name, bases, dict):
            super(_OptimizingMetaclass, cls).__init__(name, bases, dict)

            for name, attribute in dict.items():
                if type(attribute) is FunctionType:
                    dict[name] = _make_constants(attribute, builtin_only, stoplist, verbose)

    return _OptimizingMetaclass

__metaclass__ = build_optimizing_metaclass(verbose=True)

