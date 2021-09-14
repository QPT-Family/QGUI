# Author: Acer Zhang
# Datetime: 2021/9/7 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import tkinter
from tkinter import ttk
from ttkbootstrap import Style


class CreateQGUI(tkinter.Tk):
    def __init__(self, style='lumen'):
        super().__init__()
        self.title('File Search Engine')
        self.style = Style(style)
        self.a = Progressbar(self)
        self.a.pack()


class LeftTab(ttk.Frame):
    def __init__(self, max_len, *args, **kwargs):
        super().__init__()


class Progressbar(ttk.Frame):
    def __init__(self, max_len, *args, **kwargs):
        super().__init__()
        # container for user input
        input_labelframe = ttk.Labelframe(self, text='基础配置', padding=(20, 10, 10, 5))
        input_labelframe.pack(side='top', fill='x')
        input_labelframe.columnconfigure(1, weight=1)

        # file path input
        ttk.Label(input_labelframe, text='选择文件').grid(row=0, column=0, padx=10, pady=2, sticky='ew')
        e1 = ttk.Entry(input_labelframe)
        e1.grid(row=0, column=1, sticky='ew', padx=10, pady=2)
        b1 = ttk.Button(input_labelframe, text='选择文件夹', command=None, style='primary.TButton')
        b1.grid(row=0, column=2, sticky='ew', pady=2, ipadx=10)

        # search term input
        ttk.Label(input_labelframe, text='输出目录').grid(row=1, column=0, padx=10, pady=2, sticky='ew')
        e2 = ttk.Entry(input_labelframe)
        e2.grid(row=1, column=1, sticky='ew', padx=10, pady=2)
        b2 = ttk.Button(input_labelframe, text='选择文件夹', command=None, style='primary.Outline.TButton')
        b2.grid(row=1, column=2, sticky='ew', pady=2)

        terminal = tkinter.Text(self)
        terminal.pack()

        self.progressbar = ttk.Progressbar(self,
                                           length=500,
                                           maximum=100,
                                           style='Striped.Horizontal.TProgressbar')
        self.progressbar.pack(fill='y')
        self.progressbar["value"] = 10



