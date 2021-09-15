# Author: Acer Zhang
# Datetime: 2021/8/31 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import tkinter
from tkinter import ttk
from ttkbootstrap import Style

from qgui.manager import QStyle


class CreateQGUI(tkinter.Tk):
    def __init__(self,
                 title="未命名应用",
                 style=QStyle.default):
        super().__init__()
        self.title(title)
        self.style = Style()
        self.style.configure('bg.TFrame', background=self.style.colors.inputbg)
        self.style.configure('bg.TLabel', background=self.style.colors.inputbg)
        self.geometry("940x520")
        self.wm_resizable(False, False)


if __name__ == '__main__':
    CreateQGUI().mainloop()
