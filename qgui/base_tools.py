# Author: Acer Zhang
# Datetime:2021/9/21 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import tkinter


def select_var_dtype(dtype):
    if issubclass(dtype, int):
        return tkinter.IntVar
    elif issubclass(dtype, float):
        return tkinter.DoubleVar
    elif issubclass(dtype, str):
        return tkinter.StringVar
    elif issubclass(dtype, bool):
        return tkinter.BooleanVar
