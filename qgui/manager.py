# Author: Acer Zhang
# Datetime: 2021/9/14 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os

from tkinter import messagebox

import qgui

QGUI_BASE_PATH = os.path.dirname(qgui.__file__)
RESOURCES_PATH = os.path.join(QGUI_BASE_PATH, "resources")
ICON_PATH = os.path.join(RESOURCES_PATH, "icon")


class QStyle:
    default = None
    lumen = "lumen"
    # 以下需后期重新定制颜色方案
    paddle = "cosmo"


class MessageBox:
    @staticmethod
    def info(text: str, title: str = "消息 - QGUI"):
        messagebox.showinfo(title, text)

    @staticmethod
    def warning(text: str, title: str = "警告 - QGUI"):
        messagebox.showwarning(title, text)

    @staticmethod
    def erroe(text: str, title: str = "错误 - QGUI"):
        messagebox.showerror(title, text)



