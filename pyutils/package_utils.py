import os

__version__ = [0, 0, 0]
__release__ = False                         # False for nightly
__versionSub__ = "Alpha/Test"               # Short version description

def getVersionDigitsStr():
    """
    String representation of the version number only (no additional info)
    Inspired by the Makehuman Project
    """
    return ".".join( [str(v) for v in __version__] )

def _versionStr():
    """
    Inspired by the Makehuman Project
    """
    if __versionSub__:
        return getVersionDigitsStr() + " " + __versionSub__
    else:
        return getVersionDigitsStr()

def isRelease():
    """
    True when release version, False for nightly (dev) build
    Inspired by the Makehuman Project
    """
    return __release__

def isBuild():
    """
    Determine whether the app is frozen using pyinstaller/py2app.
    Returns True when this is a release or nightly build (eg. it is build as a
    distributable package), returns False if it is a source checkout.
    Inspired by the Makehuman Project
    """
    return getattr(sys, 'frozen', False)

def getVersion():
    """
    Comparable version as list of ints
    Inspired by the Makehuman Project
    """
    return __version__

def getVersionStr(verbose=True):
    """
    Verbose version as string, for displaying and information
    Inspired by the Makehuman Project
    """
    if isRelease():
        return _versionStr()
    else:
        try:
            result = _versionStr() + " (r%s %s)" % (os.environ['HGREVISION'], os.environ['HGNODEID'])
            if verbose:
                result += (" [%s]" % os.environ['HGREVISION_SOURCE'])
            return result
        except KeyError:
            print("HG lib does not seem to be installed.")

def getShortVersion():
    """
    Useful for tagging assets
    Inspired by the Makehuman Project
    """
    if __versionSub__:
        return __versionSub__.replace(' ', '_').lower()
    else:
        return "v" + getVersionDigitsStr()

