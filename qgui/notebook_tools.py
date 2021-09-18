# Author: Acer Zhang
# Datetime: 2021/9/16 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import os
import threading
import traceback
from typing import List

import tkinter
from tkinter import ttk
from tkinter import filedialog

from qgui.manager import ICON_PATH, FONT

RUN_ICON = os.path.join(ICON_PATH, "play_w.png")

LEFT_PAD_LEN = 10
INPUT_BOX_LEN = 86


class BaseNotebookTool:
    """
    基础Notebook工具集，提供基础异步Clallback
    若需返回信息，请重写get_info方法->{name:info闭包}
    """

    def __init__(self,
                 bind_func=None,
                 name=None,
                 style="primary",
                 tab_index=0,
                 async_run=False,
                 allow_concurrency=False):
        if bind_func and not hasattr(bind_func, "__call__"):
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
        self.name = name
        self.style = style
        self.tab_index = tab_index
        self.async_run = async_run
        self.allow_concurrency = allow_concurrency

        # 占位符
        self.global_info = None
        self.master = None

        # 避免重复点击的Flag
        self.async_run_event = threading.Event()

    def _callback(self, func, start_func=None, end_func=None):
        if not self.async_run:
            def render():
                if start_func:
                    start_func()
                func(self.global_info)
                if end_func:
                    end_func()
        else:
            def render():
                if start_func:
                    # 若不允许并发则在启动时加Flag
                    if not self.allow_concurrency:
                        if self.async_run_event.is_set():
                            return lambda: print("当前设置为禁止并发，请勿重复点击")
                        else:
                            self.async_run_event.set()
                    start_func()

                def new_func(obj):
                    try:
                        func(obj)
                    except Exception as e:
                        print("-----以下为异常信息-----")
                        print(traceback.print_exc())
                        print("-----以上为异常信息-----")
                    if end_func:
                        end_func()
                    # 清除Flag，此时按钮可以再次点击
                    self.async_run_event.clear()

                t = threading.Thread(target=new_func, args=(self.global_info,))
                t.setDaemon(True)
                t.start()
        return render

    def build(self, *args, **kwargs):
        self.global_info = kwargs["global_info"]
        self.master = kwargs["master"]

    def get_info(self) -> dict:
        return dict()


class BaseChooseFileTextButton(BaseNotebookTool):
    def __init__(self,
                 bind_func=None,
                 name=None,
                 label_info: str = "目标文件路径",
                 entry_info: str = "请选择文件路径",
                 button_info: str = "选 择 文 件 ",
                 style="primary",
                 tab_index=0):
        super().__init__(bind_func, name=name, style=style, tab_index=tab_index)

        self.label_info = label_info
        self.button_info = button_info
        self.name = name

        self.entry_var = tkinter.StringVar(value=entry_info)

    def _callback(self, func, start_func=None, end_func=None):
        if not hasattr(self, "filetypes"):
            self.filetypes = [('All Files', '*')]

        def render():
            file_path = filedialog.askopenfilename(title="选择文件",
                                                   filetypes=self.filetypes)
            if file_path:
                self.entry_var.set(file_path)
            return func(file_path)

        return render

    def build(self, **kwargs) -> tkinter.Frame:
        super().build(**kwargs)
        frame = ttk.Frame(self.master, style="TFrame")
        frame.pack(side="top", fill="x", padx=5, pady=2)
        label = ttk.Label(frame,
                          text=self.label_info,
                          style="TLabel",
                          width=16)
        label.pack(side="left")
        entry = ttk.Entry(frame,
                          style=self.style + ".info.TEntry",
                          textvariable=self.entry_var)
        entry.pack(side="left", fill="x", expand="yes", padx=5, pady=2)

        command = self._callback(self.bind_func) if self.bind_func else self._callback(lambda x: print(f"文件{x}被选取"))
        button = ttk.Button(frame,
                            text=self.button_info,
                            style=self.style + ".TButton",
                            command=command,
                            width=12)
        button.pack(side="right")
        return frame

    def get_info(self) -> dict:
        field = self.name if self.name else self.__class__.__name__

        def reader():
            return self.entry_var.get()

        return {field: reader}


class ChooseFileTextButton(BaseChooseFileTextButton):
    def __init__(self,
                 bind_func=None,
                 name=None,
                 label_info: str = "目标文件路径",
                 entry_info: str = "请选择文件路径",
                 button_info: str = "选 择 文 件",
                 filetypes=None,
                 style="primary",
                 tab_index=0):
        self.filetypes = [('All Files', '*')] if filetypes is None else filetypes

        super().__init__(bind_func=bind_func,
                         name=name,
                         label_info=label_info,
                         entry_info=entry_info,
                         button_info=button_info,
                         style=style,
                         tab_index=tab_index)


class ChooseDirTextButton(BaseChooseFileTextButton):
    def __init__(self,
                 bind_func=None,
                 name=None,
                 label_info: str = "目标文件夹路径",
                 entry_info: str = "请选择文件夹路径",
                 button_info: str = "选择文件夹",
                 style="primary",
                 tab_index=0):
        super().__init__(bind_func=bind_func,
                         name=name,
                         label_info=label_info,
                         entry_info=entry_info,
                         button_info=button_info,
                         style=style,
                         tab_index=tab_index)

    def _callback(self, func, start_func=None, end_func=None):
        def render():
            file_path = filedialog.askdirectory(title="选择文件夹")
            if file_path:
                self.entry_var.set(file_path)
            return func(file_path)

        return render


class RunButton(BaseNotebookTool):
    def __init__(self, bind_func, text="开始执行", async_run=True, style="primary", tab_index=0, allow_concurrency=False):
        super(RunButton, self).__init__(bind_func,
                                        style,
                                        tab_index=tab_index,
                                        async_run=async_run,
                                        allow_concurrency=allow_concurrency)
        self.text = text

        self.icon = None

    def build(self, **kwargs) -> tkinter.Frame:
        super(RunButton, self).build(**kwargs)
        frame = ttk.Frame(self.master, style="TFrame")
        frame.pack(side="top", fill="x", padx=5, pady=5)
        self.icon = tkinter.PhotoImage(name=self.text,
                                       file=RUN_ICON)

        def click_btn():
            self.btn.configure(style="secondary.TButton")

        def done_btn():
            self.btn.configure(style="success.TButton")

        self.btn = ttk.Button(frame,
                              text=self.text,
                              image=self.text,
                              compound='left',
                              command=self._callback(self.bind_func, click_btn, done_btn),
                              style="success.TButton",
                              width=10)

        self.btn.pack(anchor="ne", padx=0, pady=0)
        return frame


class InputBox(BaseNotebookTool):
    def __init__(self,
                 name=None,
                 default="请在此输入",
                 label_info="输入信息",
                 style="primary",
                 tab_index=0):
        super().__init__(name=name,
                         style=style,
                         tab_index=tab_index)
        self.input_vars = tkinter.StringVar(value=default)
        self.label_info = label_info

    def build(self, **kwargs):
        super().build(**kwargs)
        frame = ttk.Frame(self.master, style="TFrame")
        frame.pack(side="top", fill="x", padx=5, pady=5)
        label = ttk.Label(frame,
                          text=self.label_info,
                          style="TLabel",
                          width=16)
        label.pack(side="left")

        entry = ttk.Entry(frame,
                          style=self.style + ".info.TEntry",
                          textvariable=self.input_vars,
                          width=INPUT_BOX_LEN)
        entry.pack(side="left", fill="x", padx=5, pady=2)
        return frame

    def get_info(self) -> dict:
        field = self.name if self.name else self.__class__.__name__

        def render():
            return self.input_vars.get()

        return {field: render}


class Combobox(BaseNotebookTool):
    def __init__(self,
                 name=None,
                 title: str = None,
                 options: List[str] = None,
                 style="custom",
                 tab_index=0):
        super().__init__(name=name,
                         style=style,
                         tab_index=tab_index)
        self.title = title
        self.options = options

        self.options = options if options else ["--请选择--"]

    def build(self, **kwargs):
        super().build(**kwargs)
        frame = ttk.Frame(self.master, style="TFrame")
        frame.pack(side="top", fill="x", padx=5, pady=5)
        label = ttk.Label(frame,
                          text=self.title,
                          style="TLabel",
                          width=16)
        label.pack(side="left")
        self.comb = ttk.Combobox(self.master,
                                 style=self.style + ".TCombobox",
                                 values=self.options)
        self.comb.current(0)

        self.comb.pack(side="left", fill="x", padx=5, pady=2)

        return frame

    def get_info(self) -> dict:
        field = self.name if self.name else self.__class__.__name__

        def render():
            return self.comb.get()

        return {field: render}
