# Author: Acer Zhang
# Datetime: 2021/9/7 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import tkinter
from tkinter import ttk
from ttkbootstrap import Style


class Application(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title('File Search Engine')
        self.style = Style('lumen')
        self.a = SearchEngine(self)
        self.a.pack()


class SearchEngine(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super(SearchEngine, self).__init__()
        self.progressbar = ttk.Progressbar(self,
                                           length=500,
                                           style='Striped.Horizontal.TProgressbar')
        self.progressbar.pack(fill='y')
        self.progressbar["value"] = 10


Application().mainloop()
