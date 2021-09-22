# Author: Acer Zhang
# Datetime:2021/9/21 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
from typing import Dict

import tkinter

from qgui.manager import ConcurrencyModeFlag


def check_callable(bind_func):
    if bind_func and not hasattr(bind_func, "__call__"):
        if hasattr(bind_func, "__name__"):
            name = bind_func.__name__
        else:
            name = bind_func
        raise Exception(f"{name}的bind_func不能被调用，其至少需要具备__call__方法，建议在此传入函数/方法或自行构建具备__call__方法的对象。\n"
                        f"Example:\n"
                        f"    def xxx():\n"
                        f"        Do sth\n"
                        f"    MakeThisTool(bind_func=xxx)\n"
                        f"Error example:\n"
                        f"    def xxx():\n"
                        f"        Do sth\n"
                        f"    MakeThisTool(bind_func=xxx())")


class ArgInfo:
    def __init__(self, name=None, set_func=None, get_func=None):
        if not name and (set_func or get_func):
            raise Exception(f"请设置{self.__class__.__name__}的name")
        if name:
            self.all_info = {name: self}
        else:
            self.all_info = dict()

        check_callable(set_func)
        check_callable(get_func)
        self.set_func = set_func
        self.get_func = get_func

    def set(self, *args, **kwargs):
        return self.set_func(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.get_func(*args, **kwargs)

    def get_info(self):
        return self.all_info

    def __add__(self, other):
        other_info = other.all_info
        if other_info:
            for info_name in other_info:
                if info_name in self.all_info:
                    self.all_info[f"{info_name}-QGUI-Conflict-Field-{len(self.all_info)}"] = other_info[info_name]
                else:
                    self.all_info[info_name] = other_info[info_name]
        return self


def select_var_dtype(dtype):
    if issubclass(dtype, int):
        return tkinter.IntVar
    elif issubclass(dtype, float):
        return tkinter.DoubleVar
    elif issubclass(dtype, str):
        return tkinter.StringVar
    elif issubclass(dtype, bool):
        return tkinter.BooleanVar


if __name__ == '__main__':
    n = ArgInfo(set_func=lambda: print("a"))
    a = ArgInfo("A", None, lambda: print("a"))
    b = ArgInfo("B", None, lambda: print("b"))
    c = ArgInfo("A", None, lambda: print("a"))
    n += a + b + c
    a.get()
    pass
