# Author: Acer Zhang
# Datetime: 2021/8/31 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import tkinter
from tkinter import ttk
from ttkbootstrap import Style

from qgui.manager import QStyle


class BaseBanner:
    pass


class BaseTab:
    pass


class BaseModule:
    pass


class CreateQGUI(tkinter.Tk):
    def __init__(self,
                 title="未命名应用",
                 style=QStyle.default):
        super().__init__()
        self.title(title)
        self.style = Style(style)


if __name__ == '__main__':
    CreateQGUI().mainloop()
