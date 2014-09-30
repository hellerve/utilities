import re
import os
import sys
import imp

from inspect import Parameter, Signature
from collections import OrderedDict
from xml.etree.ElementTree import parse


def make_signature(names):
    """Generates signatures for a bunch of variables."""
    return Signature(Parameter(name, Parameter.POSITIONAL_OR_KEYWORD)
                     for name in names)


def _make_init(fields):
    """Code generator for an init function."""
    code = "def __init__(self, %s):\n" % ','.join(fields)
    for name in fields:
        code += '   self.%s = %s\n' % (name, name)
    return code


def _xml_to_code(filename):
    """Code generator for an XML tree."""
    doc = parse(filename)
    code = "from breaking_python import *\n"
    for field in doc.findall('field'):
        code += _xml_field_code(field)
    return code


def _xml_field_code(field):
    """Code generator for an XML element."""
    name = field.get('name')
    code = "class %s(Field):\n" % name
    for element in field.findall('element'):
        dtype = element.get('type')
        options = ['%s = %s' % (key, val) for key, val in element.items()
                   if key != 'type']
        name = element.text.strip()
        code += '    %s = %s(%s)\n' % (name, dtype, ','.join(options))
    return code


def _make_setter(dcls):
    """Code generator for setter functions."""
    code = 'def __set__(self, instance, value):\n'
    for d in dcls.__mro__:
        if 'set_code' in d.__dict__:
            for line in d.set_code():
                code += '    ' + line + '\n'
    return code


def _install_importer():
    sys.meta_path.append(Finder())


class Finder:
    """Custom module finder for xml files."""
    @classmethod
    def find_module(cls, fullname, path):
        for dirname in sys.path:
            filename = os.path.join(dirname, fullname + '.xml')
            if os.path.exists(filename):
                return StructXMLLoader(filename)


class StructXMLLoader:
    def __init__(self, filename):
        self.filename = filename

    def load_module(self, fullname):
        if fullname in sys.modules:
            mod = sys.modules[fullname]
        else:
            mod = imp.new_module(fullname)
            sys.modules[fullname] = mod
        mod.__file__ = self.filename
        mod.__loader__ = self
        code = _xml_to_code(self.filename)
        exec(code, mod.__dict__, mod.__dict__)
        return mod


class DescriptorMeta(type):
    """Meta class that implements the magic behind the descriptor class."""
    def __init__(self, clsname, bases, clsdict):
        super().__init__(clsname, bases, clsdict)
        if '__set__' in clsdict:
            raise TypeError("Use set_code(), not __set__()")
        code = _make_setter(self)
        exec(code, globals(), clsdict)
        setattr(self, '__set__', clsdict['__set__'])


class Descriptor(metaclass=DescriptorMeta):
    """Base class that implements custom set and delete functions."""
    def __init__(self, name=None):
        self.name = name

    @staticmethod
    def set_code():
        return ['instance.__dict__[self.name] = value']

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class Typed(Descriptor):
    """Base class that implements static typing."""
    ty = object

    @staticmethod
    def set_code():
        return ['if not isinstance(value, self.ty):',
                '   raise TypeError("Expected %s" % self.ty)']


class Integer(Typed):
    ty = int


class Float(Typed):
    ty = float


class String(Typed):
    ty = str


class Dictionary(Typed):
    ty = dict


class Array(Typed):
    ty = list


class Set(Typed):
    ty = set


class Sized(Descriptor):
    def __init__(self, *args, maxlen, **kwargs):
        self.maxlen = maxlen
        super().__init__(*args, **kwargs)

    @staticmethod
    def set_code():
        return ['if len(value) > self.maxlen:',
                '    raise ValueError("Must be >= %s" % self.maxlen)']


class SizedString(String, Sized):
    pass


class Regex(Descriptor):
    def __init__(self, *args, pat, **kwargs):
        self.pat = re.compile(pat)
        super().__init__(*args, **kwargs)

    @staticmethod
    def set_code():
        return ['if not self.pat.match(value):'
                '    raise ValueError("Invalid string")']


class SizedRegexString(SizedString, Regex):
    pass


class FieldMeta(type):
    """
    Metaclass that does the magic for fields.
    Use at your own risk.
    """
    @classmethod
    def __prepare__(cls, name, bases):
        return OrderedDict()

    def __new__(cls, name, bases, clsdict):
        fields = [key for key, val in clsdict.items()
                  if isinstance(val, Descriptor)]
        for name in fields:
            clsdict[name].name = name

        if fields:
            exec(_make_init(fields), globals(), clsdict)
        clsobj = super().__new__(cls, name, bases, dict(clsdict))
        sig = make_signature(clsobj._fields)
        setattr(clsobj, '__signature__', sig)
        return clsobj


class Field(metaclass=FieldMeta):
    """
    Utility class that makes instance variables
    codable as strings.
    Usable as follows:
    class MyString(Fields):
        length = Integer()
        stringed = SizedString(maxlen=self.length)
    You can even structure you code as XML and import it like python.
    """
    _fields = []

_install_importer()
