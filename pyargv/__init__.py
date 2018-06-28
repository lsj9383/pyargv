import os
import sys
from functools import wraps
from flask import Flask

class BaseArgv:
    def __init__(self, key, default, valtype):
        self.__key__ = key
        self.__default__ = default
        self.__type__ = valtype

    @property
    def key(self):
        return self.__key__

    @property
    def default(self):
        return self.__default__

    @property
    def valtype(self):
        return self.__type__

# 普通参数
class Argv(BaseArgv):
    def __init__(self, key, default=None, valtype=str):
        super().__init__(key, default, valtype)

# 布尔型参数
class Boolean(BaseArgv):
    def __init__(self, key, default=False):
        super().__init__(key, default, bool)

# kv对参数
class KeyValue(BaseArgv):
    def __init__(self, key, nick=None, default=None, valtype=str):
        super().__init__(key, default, valtype)
        self.__nick__ = nick

    @property
    def nick(self):
        return self.__nick__

# 根据kv对的nick重构输入的命令行参数
def __refactor_cmdargv__(kv_argvlist):
    argvline = " ".join(sys.argv[1:])
    for argv in kv_argvlist:
        argvline = argvline.replace(argv.nick+" ", argv.key+":")
    cmdargv = argvline.split(" ")
    return cmdargv

# 将参数的默认值进行载入
__normal_argv_keys__ = []
def __load_default__(kws, norm_argvlist, bool_argvlist, kv_argvlist):
    for argv in norm_argvlist:
        kws[argv.key] = argv.default
        __normal_argv_keys__.append(argv.key)
    for argv in bool_argvlist:
        kws[argv.key] = argv.default
    for argv in kv_argvlist:
        kws[argv.key] = argv.default

# kws填充
def __fill_kws__(kws, normargs, boolargs, mapargs):
    for idx, argv in enumerate(normargs):
        key = __normal_argv_keys__[idx]
        kws[key] = normargs[idx]
    for argv in boolargs:
        kws[argv[2:]] = True if argv[2:] in argv else kws[argv[2:]]
    for argv in mapargs:
        parts = argv.split(":")
        key = parts[0]
        val = ":".join(parts[1:])
        if key in kws:
            kws[key] = val

# 构造kws
def __kwsload__(kws, norm_argvlist, bool_argvlist, kv_argvlist):
    cmdargv = __refactor_cmdargv__(kv_argvlist)

    # 命令行参数类型区分
    normargs = [argv for argv in cmdargv if (not argv.startswith("--")) and (not ":" in argv)]
    boolargs = [argv for argv in cmdargv if argv.startswith("--")]
    mapargs = [argv for argv in cmdargv if ":" in argv]

    # kws中载入参数的默认值
    __load_default__(kws, norm_argvlist, bool_argvlist, kv_argvlist)

    # kws中载入实际参数
    __fill_kws__(kws, normargs, boolargs, mapargs)

def __verify__(argvlist):
    s = set()
    if (not isinstance(argvlist, tuple)) and (not isinstance(argvlist, list)):
        raise Exception("should input tuple or list")

    for argv in argvlist:
        # tuple or list中的元素不是BaseArgv
        if not isinstance(argv, BaseArgv):
            raise Exception("the argv element not is BaseArgv")

        # BaseArgv同key
        if argv.key in s:
            raise Exception("can't use the same key")
        s.add(argv.key)

__unique__ = 0
def parse(argvlist=(), help=False):
    global __unique__
    if __unique__:
        raise Exception("'parse'方法仅能调用一次")
    __unique__ = 1
    # 检验参数构造
    __verify__(argvlist)

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