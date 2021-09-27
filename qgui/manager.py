# Author: Acer Zhang
# Datetime: 2021/9/14 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os
import platform

from tkinter import messagebox

import qgui

# 资源部分
QGUI_BASE_PATH = os.path.dirname(qgui.__file__)
RESOURCES_PATH = os.path.join(QGUI_BASE_PATH, "resources")
ICON_PATH = os.path.join(RESOURCES_PATH, "icon")

HORIZONTAL = "Horizontal水平方向"
VERTICAL = "Vertical垂直方向"


# Tools部分
class ConcurrencyModeFlag:
    # QUEUE_ = "触发后相关事件会以队列的形式执行"
    SAFE_CONCURRENCY_MODE_FLAG = "不允许并发，禁止触发下一个事件"
    # FORCE_CONCURRENCY_MODE_FLAG = "不允许并发，下一个事件被触发时结束上一个事件"


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


def show_file_or_path(path):
    if platform.system().lower() == "darwin":
        import subprocess
        subprocess.call(["open", path])
    else:
        os.startfile(path)


BLACK = "#24262d"
GRAY = "#e3e3e3"
GREEN = "#76b67e"
FONT = "黑体"
