# Author: Acer Zhang
# Datetime: 2021/9/16 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import os

import tkinter
from tkinter import ttk
from tkinter.filedialog import askopenfilename

from qgui.manager import ICON_PATH

RUN_ICON = os.path.join(ICON_PATH, "play_w.png")


class BaseNotebookTool:
    def __init__(self,
                 bind_func,
                 style="primary",
                 tab_index=0):
        if not hasattr(bind_func, "__call__"):
            raise f"{__class__.__name__}的bind_func需具备__call__方法，建议在此传入函数对象或自行构建具备__call__方法的对象。\n" \
                  f"Example:\n" \
                  f"    def xxx():\n" \
                  f"        Do sth\n" \
                  f"    MakeThisTool(bind_func=xxx)\n" \
                  f"Error example:\n" \
                  f"    def xxx():\n" \
                  f"        Do sth\n" \
                  f"    MakeThisTool(bind_func=xxx())"
        self.bind_func = bind_func
        self.style = style
        self.tab_index = tab_index

    def build(self, *args, **kwargs) -> tkinter.Frame:
        pass


class ChooseFileTextButton(BaseNotebookTool):
    def __init__(self,
                 bind_func,
                 label_info: str = "目标文件路径：",
                 entry_info: str = "请选择文件路径",
                 button_info: str = "选择文件",
                 style="primary",
                 tab_index=0):
        super(ChooseFileTextButton, self).__init__(bind_func, style, tab_index=tab_index)

        self.label_info = label_info
        self.button_info = button_info

        self.entry_var = tkinter.StringVar(value=entry_info)

    def _callback(self, func):
        def render():
            file_path = askopenfilename(title="选择文件",
                                        filetypes=[('All Files', '*')])
            if file_path:
                self.entry_var.set(file_path)
            return func(file_path)

        return render

    def build(self, master) -> tkinter.Frame:
        frame = ttk.Frame(master, style="TFrame")
        frame.pack(side="top", fill="x", padx=5, pady=2)
        label = ttk.Label(frame,
                          text=self.label_info,
                          style="TLabel")
        label.pack(side="left")
        entry = ttk.Entry(frame,
                          style=self.style + ".info.TEntry",
                          textvariable=self.entry_var)
        entry.pack(side="left", fill="x", expand="yes", padx=5, pady=2)

        button = ttk.Button(frame,
                            text=self.button_info,
                            style=self.style + ".TButton",
                            command=self._callback(self.bind_func))
        button.pack(side="right")
        return frame


class RunButton(BaseNotebookTool):
    def __init__(self, bind_func, text="开始执行", style="primary", tab_index=0):
        super(RunButton, self).__init__(bind_func, style, tab_index=tab_index)
        self.text = text

        self.icon = None

    def build(self, master) -> tkinter.Frame:
        frame = ttk.Frame(master, style="TFrame")
        frame.pack(side="top", fill="x", padx=5, pady=5)
        self.icon = tkinter.PhotoImage(name=self.text,
                                       file=RUN_ICON)
        btn = ttk.Button(frame,
                         text=self.text,
                         image=self.text,
                         compound='left',
                         command=self.bind_func,
                         style="success.TButton")

        btn.pack(anchor="ne", padx=0, pady=1)
        return frame
