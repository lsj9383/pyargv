import os
from functools import wraps
from flask import Flask

def __around__(f):
    pass

def argvlist():
    def wrapper(f):
        @wraps(f)
        def inner(*args, **kws):
             return __around__(f)
        return inner
    return wapper