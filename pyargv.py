import os
import sys
from functools import wraps
from flask import Flask

class BaseArgv:
    def __init__(self, key, default):
        self.__key__ = key
        self.__default__ = default

    @property
    def key(self):
        return self.__key__

    @property
    def default(self):
        return self.__default__

class Argv(BaseArgv):
    def __init__(self, key, default=None):
        super().__init__(key, default)
        
class Boolean(BaseArgv):
    def __init__(self, key, default=False):
        super().__init__(key, default)

def __kwsload__(kws, norm_argvlist, bool_argvlist):
    normargs = [argv for argv in sys.argv[1:] if not argv.startswith("--")]
    boolargs = [argv for argv in sys.argv[1:] if argv.startswith("--")]
    for idx, argv in enumerate(norm_argvlist):
        kws[argv.key] = normargs[idx] if idx < len(normargs) else argv.default

    for idx, argv in enumerate(bool_argvlist):
        kws[argv.key] = argv.default
    for argv in boolargs:
        kws[argv[2:]] = True if argv[2:] in argv else kws[argv[2:]]

    

def argvload(argvlist=()):
    bool_argvlist = [argv for argv in argvlist if isinstance(argv, Boolean)]
    norm_argvlist = [argv for argv in argvlist if isinstance(argv, Argv)]
    def wrapper(f):
        @wraps(f)
        def inner(*args, **kws):
            __kwsload__(kws, norm_argvlist, bool_argvlist)
            return f(*args, **kws)
        return inner
    return wrapper