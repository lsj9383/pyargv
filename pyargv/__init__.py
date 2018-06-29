import os
import sys
from functools import wraps

# 抽象参数
class BaseArgv:
    def __init__(self, key, default, *, valtype, ed=None):
        self.__key__ = key
        self.__default__ = default
        self.__type__ = valtype
        # error-description 缺少该参数时的错误描述信息
        self.__ed__ = ed if ed else "missing 1 required argument:'{key}'".format(key=key)

    @property
    def key(self):
        return self.__key__

    @property
    def default(self):
        return self.__default__

    @property
    def valtype(self):
        return self.__type__

    @property
    def ed(self):
        return self.__ed__

# 普通参数
class Argv(BaseArgv):
    def __init__(self, key, default=None, *, valtype=str, ed=None):
        super().__init__(key, default=default, valtype=valtype, ed=ed)

# 布尔型参数
class Boolean(BaseArgv):
    def __init__(self, key):
        super().__init__(key, default=False, valtype=bool, ed=None)

# kv对参数
class KeyValue(BaseArgv):
    def __init__(self, key, nick=None, default=None, *, valtype=str, ed=None):
        super().__init__(key, default=default, valtype=valtype, ed=ed)
        self.__nick__ = nick

    @property
    def nick(self):
        return self.__nick__

# 根据kv对的nick重构输入的命令行参数
def __refactor_cmdargv__(kv_argvlist):
    argvline = " ".join(sys.argv[1:])
    for argv in kv_argvlist:
        argvline = argvline.replace(argv.nick+" ", argv.key+":")
    cmdargv = argvline.split(" ") if argvline else []
    return cmdargv

# 将参数的默认值进行载入
__argv_keys__ = []
__argv_cache__ = {}
def __load_default__(kws, norm_argvlist, bool_argvlist, kv_argvlist):
    for argv in norm_argvlist:
        kws[argv.key] = argv.default
        __argv_cache__[argv.key] = argv
        __argv_keys__.append(argv.key)
    for argv in bool_argvlist:
        kws[argv.key] = argv.default
        __argv_cache__[argv.key] = argv
        __argv_keys__.append(argv.key)
    for argv in kv_argvlist:
        kws[argv.key] = argv.default
        __argv_cache__[argv.key] = argv
        __argv_keys__.append(argv.key)

# kws填充
def __fill_kws__(kws, normargs, boolargs, mapargs):
    for idx, argv in enumerate(normargs):
        key = __argv_keys__[idx]
        kws[key] = normargs[idx]
    for argv in boolargs:
        kws[argv[2:]] = True if argv[2:] in argv else kws[argv[2:]]
    for argv in mapargs:
        parts = argv.split(":")
        key = parts[0]
        val = ":".join(parts[1:])
        if key in kws:
            kws[key] = val

# 检查是否缺少参数
def __verify_missing_argv__(kws):
    for k in __argv_keys__:
        if kws[k] is None:
            raise Exception(__argv_cache__[k].ed)

# 构造kws
def __kwsload__(kws, norm_argvlist, bool_argvlist, kv_argvlist):
    # 重构命令行参数(根据kv参数的nick进行替换)
    cmdargv = __refactor_cmdargv__(kv_argvlist)

    # 命令行参数类型区分
    normargs = [argv for argv in cmdargv if (not argv.startswith("--")) and (not ":" in argv)]
    boolargs = [argv for argv in cmdargv if argv.startswith("--")]
    mapargs = [argv for argv in cmdargv if ":" in argv]

    # kws中载入参数的默认值
    __load_default__(kws, norm_argvlist, bool_argvlist, kv_argvlist)

    # kws中载入实际参数
    __fill_kws__(kws, normargs, boolargs, mapargs)

    # 验证是否有未输入的参数
    __verify_missing_argv__(kws)

# 检查参数构造的合法性
def __verify__(argvlist):
    s = set()
    # 1).检查参数是否为tuple
    if (not isinstance(argvlist, tuple)) and (not isinstance(argvlist, list)):
        raise Exception("should input tuple or list")

    for argv in argvlist:
        # 2).tuple or list中的元素不是BaseArgv
        if not isinstance(argv, BaseArgv):
            raise Exception("the argv element not is BaseArgv")

        # 3).BaseArgv同key
        if argv.key in s:
            raise Exception("can't use the same key")
        s.add(argv.key)

__unique__ = 0
def parse(*argvlist, help=False):
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