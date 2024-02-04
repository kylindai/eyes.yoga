import os
import io
import ast
import sys
import importlib.util

from typing import Dict, List, Tuple, Callable


class AttrDict(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except Exception as e:
            return None


class CacheUtil:

    cache = {}

    @staticmethod
    def put(key: str, value: object):
        CacheUtil.cache[key] = value

    @staticmethod
    # @lru_cache(None)
    def get(key: str):
        if key in CacheUtil.cache:
            return CacheUtil.cache[key]


class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self, *args, **kwargs):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls(*args, **kwargs)
        return self._instance[self._cls]

    def __getattr__(self, name):
        return getattr(self._instance[self._cls], name)


class ModuleUtil:

    @staticmethod
    def load_module(module_name: str, source_code: str, load_func: str = None):
        try:
            # create a file-like buffer
            buffer = io.StringIO(source_code)
            buffer.seek(0)
            # load module
            spec = importlib.util.spec_from_loader(module_name,
                                                   loader=None,
                                                   origin="memory")
            module = importlib.util.module_from_spec(spec)
            exec(source_code, module.__dict__)
            # spec.loader.exec_module(module)
            # add module to search path
            sys.modules[module_name] = module
            if load_func:
                if hasattr(module, load_func):
                    func = getattr(module, load_func)
                    return func()
            else:
                return module
        except Exception as ex:
            # print(ex)
            return None
