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

class KeyValue(BaseArgv):
    def __init__(self, key, nick=None, default=None):
        super().__init__(key, default)
        self.__nick__ = nick

    @property
    def nick(self):
        return self.__nick__

def __kwsload__(kws, norm_argvlist, bool_argvlist, kv_argvlist):
    argvline = " ".join(sys.argv[1:])
    for argv in kv_argvlist:
        argvline = argvline.replace(argv.nick+" ", argv.key+":")
    cmdargv = argvline.split(" ")
    normargs = [argv for argv in cmdargv if not argv.startswith("--")]
    boolargs = [argv for argv in cmdargv if argv.startswith("--")]
    mapargs = [argv for argv in cmdargv if ":" in argv]
    for idx, argv in enumerate(norm_argvlist):
        kws[argv.key] = normargs[idx] if idx < len(normargs) else argv.default

    for idx, argv in enumerate(bool_argvlist):
        kws[argv.key] = argv.default

    for argv in kv_argvlist:
        kws[argv.key] = argv.default

    for argv in boolargs:
        kws[argv[2:]] = True if argv[2:] in argv else kws[argv[2:]]
    for argv in mapargs:
        parts = argv.split(":")
        key = parts[0]
        val = ":".join(parts[1:])
        if key in kws:
            kws[key] = val
    
__unique__ = 0
def parse(argvlist=(), help=False):
    global __unique__
    if __unique__:
        raise Exception("'parse'方法仅能调用一次")
    __unique__ = 1
    # 将argvlist进行分发
    bool_argvlist = [argv for argv in argvlist if isinstance(argv, Boolean)]
    kv_argvlist = [argv for argv in argvlist if isinstance(argv, KeyValue)]
    norm_argvlist = [argv for argv in argvlist if isinstance(argv, Argv)]
    def wrapper(f):
        @wraps(f)
        def inner(*args, **kws):
            # 根据argvlist的内容，装载kws
            __kwsload__(kws, norm_argvlist, bool_argvlist, kv_argvlist)
            return f(*args, **kws)
        return inner
    return wrapper