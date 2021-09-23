# Author: Acer Zhang
# Datetime: 2021/9/16 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import os
import threading
import traceback
from typing import List, Dict, Tuple
from collections import OrderedDict

import tkinter
from tkinter import ttk
from tkinter import filedialog

from qgui.manager import *
from qgui.base_tools import ConcurrencyModeFlag, check_callable, ArgInfo, select_var_dtype

RUN_ICON = os.path.join(ICON_PATH, "play_w.png")

LEFT_PAD_LEN = 10
LABEL_WIDTH = 16
INPUT_BOX_LEN = 70


class BaseNotebookTool:
    """
    基础Notebook工具集，提供基础异步Callback
    1. 写Build，记得继承才会有self.master，继承时候传**kwargs
    2. 若需返回信息，请重写get_info方法->ArgInfo
    3. 如绑定func，需要封装Callback
    """

    def __init__(self,
                 bind_func=None,
                 name: str = None,
                 style: str = "primary",
                 tab_index: int = 0,
                 async_run: bool = False,
                 concurrency_mode=ConcurrencyModeFlag.SAFE_CONCURRENCY_MODE_FLAG):
        check_callable(bind_func)
        self.bind_func = bind_func
        self.name = name
        self.style = style + "." if style else ""
        self.tab_index = tab_index
        self.async_run = async_run
        # 控制并发模式
        self.concurrency_mode = concurrency_mode

        # 占位符
        self.global_info = None
        self.master = None

        # 重复点击的Flag
        self.async_run_event = threading.Event()
        self.thread_pool = list()

    def _callback(self, func, start_func=None, end_func=None):
        """
        支持同步和异步的Callback
        :param func: 函数对象
        :param start_func: 开始前的函数对象
        :param end_func: 结束后的函数对象
        """
        if func:
            if not self.async_run:
                def render():
                    if start_func:
                        start_func()
                    func(self.global_info.get_info())
                    if end_func:
                        end_func()
            else:
                def render():
                    # 若不允许并发则在启动时加Flag
                    if self.async_run_event.is_set():
                        if self.concurrency_mode == ConcurrencyModeFlag.SAFE_CONCURRENCY_MODE_FLAG:
                            return lambda: print("当前设置为禁止并发，请勿重复点击，因为点了也没用")
                    else:
                        self.async_run_event.set()

                    if start_func:
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

                    t = threading.Thread(target=new_func, args=(self.global_info.get_info(),))
                    t.setDaemon(True)
                    t.start()

                    self.thread_pool.append(t)
            return render
        else:
            def none():
                pass

            return none

    def build(self, *args, **kwargs):
        self.global_info = kwargs["global_info"]
        self.master = kwargs["master"]

    def get_arg_info(self) -> ArgInfo:
        return ArgInfo()


class BaseChooseFileTextButton(BaseNotebookTool):
    def __init__(self,
                 bind_func=None,
                 name: str = None,
                 label_info: str = "目标文件路径",
                 entry_info: str = "请选择文件路径",
                 button_info: str = "选 择 文 件 ",
                 style: str = "primary",
                 tab_index: int = 0,
                 async_run: bool = False):
        super().__init__(bind_func, name=name, style=style, tab_index=tab_index, async_run=async_run)

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
                          width=LABEL_WIDTH)
        label.pack(side="left")
        entry = ttk.Entry(frame,
                          style=self.style + "info.TEntry",
                          textvariable=self.entry_var)
        entry.pack(side="left", fill="x", expand="yes", padx=5, pady=2)

        command = self._callback(self.bind_func) if self.bind_func else self._callback(lambda x: print(f"文件{x}被选取"))
        button = ttk.Button(frame,
                            text=self.button_info,
                            style=self.style + "TButton",
                            command=command,
                            width=12)
        button.pack(side="right")
        return frame

    def get_arg_info(self) -> ArgInfo:
        field = self.name if self.name else self.__class__.__name__
        arg_info = ArgInfo(name=field, set_func=self.entry_var.set, get_func=self.entry_var.get)

        return arg_info


class ChooseFileTextButton(BaseChooseFileTextButton):
    def __init__(self,
                 bind_func=None,
                 name: str = None,
                 label_info: str = "目标文件路径",
                 entry_info: str = "请选择文件路径",
                 button_info: str = "选 择 文 件",
                 filetypes: bool = None,
                 style: str = "primary",
                 tab_index: int = 0,
                 async_run: bool = False):
        self.filetypes = [('All Files', '*')] if filetypes is None else filetypes

        super().__init__(bind_func=bind_func,
                         name=name,
                         label_info=label_info,
                         entry_info=entry_info,
                         button_info=button_info,
                         style=style,
                         tab_index=tab_index,
                         async_run=async_run)


class ChooseDirTextButton(BaseChooseFileTextButton):
    def __init__(self,
                 bind_func=None,
                 name=None,
                 label_info: str = "目标文件夹路径",
                 entry_info: str = "请选择文件夹路径",
                 button_info: str = "选择文件夹",
                 style: str = "primary",
                 tab_index: int = 0,
                 async_run: bool = False):
        super().__init__(bind_func=bind_func,
                         name=name,
                         label_info=label_info,
                         entry_info=entry_info,
                         button_info=button_info,
                         style=style,
                         tab_index=tab_index,
                         async_run=async_run)

    def _callback(self, func, start_func=None, end_func=None):
        def render():
            file_path = filedialog.askdirectory(title="选择文件夹")
            if file_path:
                self.entry_var.set(file_path)
            return func(file_path)

        return render


class RunButton(BaseNotebookTool):
    def __init__(self,
                 bind_func,
                 text: str = "开始执行",
                 async_run: bool = True,
                 style: str = "primary",
                 tab_index: int = 0,
                 concurrency_mode: bool = False):
        super(RunButton, self).__init__(bind_func,
                                        style,
                                        tab_index=tab_index,
                                        async_run=async_run,
                                        concurrency_mode=concurrency_mode)
        self.text = text

        self.icon = None

    def build(self, **kwargs) -> tkinter.Frame:
        super(RunButton, self).build(**kwargs)
        frame = ttk.Frame(self.master, style="TFrame")
        frame.pack(side="top", fill="x", padx=5, pady=5)
        self.icon = tkinter.PhotoImage(name=self.text,
                                       file=RUN_ICON)

        self.text_var = tkinter.StringVar(frame, value=self.text)

        def click_btn():
            self.btn.configure(style="secondary.TButton")
            self.btn.configure(state="disable")
            self.text_var.set("正在执行")

        def done_btn():
            self.btn.configure(style="success.TButton")
            self.btn.configure(state="normal")
            self.text_var.set(self.text)

        self.btn = ttk.Button(frame,
                              textvariable=self.text_var,
                              image=self.icon,
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
                          width=LABEL_WIDTH)
        label.pack(side="left")

        entry = ttk.Entry(frame,
                          style=self.style + "info.TEntry",
                          textvariable=self.input_vars,
                          width=INPUT_BOX_LEN)
        entry.pack(side="left", fill="x", padx=5, pady=2)
        return frame

    def get_arg_info(self) -> ArgInfo:
        field = self.name if self.name else self.__class__.__name__
        arg_info = ArgInfo(name=field, set_func=self.input_vars.set, get_func=self.input_vars.get)

        return arg_info


class Combobox(BaseNotebookTool):
    def __init__(self,
                 bind_func=None,
                 name=None,
                 title: str = "请下拉选择",
                 options: List[str] = None,
                 style="custom",
                 tab_index=0):
        super().__init__(bind_func=bind_func,
                         name=name,
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
                          width=LABEL_WIDTH)
        label.pack(side="left")
        self.comb = ttk.Combobox(frame,
                                 style=self.style + "TCombobox",
                                 values=self.options)
        self.comb.current(0)
        self.comb.bind('<<ComboboxSelected>>', self._callback(self.bind_func))
        self.comb.pack(side="left", padx=5, pady=2)

        return frame

    def get_arg_info(self) -> ArgInfo:
        field = self.name if self.name else self.__class__.__name__
        arg_info = ArgInfo(name=field, set_func=self.comb.set, get_func=self.comb.get)

        return arg_info


class Slider(BaseNotebookTool):
    def __init__(self,
                 name=None,
                 title: str = "请拖动滑块",
                 default: int = 0,
                 min_size: int = 0,
                 max_size: int = 100,
                 dtype=int,
                 style="primary",
                 tab_index=0):
        super().__init__(name=name,
                         style=style,
                         tab_index=tab_index)
        self.title = title
        self.default = default
        self.min_size = min_size
        self.max_size = max_size
        self.dtype = dtype

    def slider_var_trace(self, *args):
        v = self.scale.get()
        self.value_var.set(f"当前值 {self.dtype(v)}")

    def build(self, **kwargs):
        super().build(**kwargs)

        frame = ttk.Frame(self.master, style="TFrame")

        self.slider_var = select_var_dtype(self.dtype)(frame, value=self.default)
        self.value_var = tkinter.StringVar(frame, value=f"当前值 {self.default}")
        self.slider_var.trace("w", self.slider_var_trace)
        frame.pack(side="top", fill="x", padx=5, pady=5)
        label = ttk.Label(frame,
                          text=self.title,
                          style="TLabel",
                          width=LABEL_WIDTH)
        label.pack(side="left")
        self.scale = ttk.Scale(frame,
                               from_=self.min_size,
                               to=self.max_size,
                               value=self.default,
                               variable=self.slider_var,
                               length=500)
        # ToDo ttk 的Bug
        # self.scale.configure(style="info.TSlider")
        self.scale.pack(side="left", padx=5, fill="x")
        self.value = ttk.Label(frame,
                               textvariable=self.value_var,
                               style="TLabel",
                               width=LABEL_WIDTH)
        self.value.pack(side="right")
        return frame

    def get_arg_info(self) -> ArgInfo:
        field = self.name if self.name else self.__class__.__name__
        arg_info = ArgInfo(name=field, set_func=self.scale.set, get_func=self.scale.get)

        return arg_info


class BaseCheckButton(BaseNotebookTool):
    def __init__(self,
                 options: str or Tuple[str, bool] or List[Tuple[str, bool]],
                 bind_func=None,
                 name=None,
                 title="请选择",
                 style="primary",
                 button_style="TCheckbutton",
                 tab_index=0,
                 async_run=False,
                 concurrency_mode=ConcurrencyModeFlag.SAFE_CONCURRENCY_MODE_FLAG,
                 mode=None):
        super().__init__(bind_func=bind_func,
                         name=name,
                         style=style,
                         tab_index=tab_index,
                         async_run=async_run,
                         concurrency_mode=concurrency_mode)
        self.title = title
        self.mode = mode
        if isinstance(options, str):
            self.options = {options: 0}
        if isinstance(options, tuple):
            self.options = {options[0]: 1 if options[1] else 0}
        if isinstance(options, list):
            self.options = OrderedDict()
            if len(options[0]) != 2:
                raise TypeError(f"{self.__class__.__name__}的options参数需要为str or List[Tuple[str, bool]]格式\n"
                                f"Example:\n"
                                f"'选择框1' or [('选择1', 0), ('选择2', 1), ('选择3', 0)]")
            for option in options:
                self.options[option[0]] = 1 if option[1] else 0
        self.button_style = button_style

    def build(self, *args, **kwargs):
        super().build(*args, **kwargs)
        frame = ttk.Frame(self.master, style="TFrame")

        frame.pack(side="top", fill="x", padx=5, pady=5)
        label = ttk.Label(frame,
                          text=self.title,
                          style="TLabel",
                          width=LABEL_WIDTH)
        label.pack(side="left")

        self.value_vars = dict()
        for option in self.options:
            self.value_vars[option] = tkinter.StringVar(frame, value=self.options[option])
            if self.mode == "ToolButton":
                pad_x = 0
            else:
                pad_x = 5
            ttk.Checkbutton(frame,
                            text=option,
                            style=self.style + self.button_style,
                            variable=self.value_vars[option],
                            command=self._callback(self.bind_func)).pack(side="left", padx=pad_x)

    def get_arg_info(self) -> ArgInfo:
        field = self.name if self.name else self.__class__.__name__
        arg_info = ArgInfo()
        for v in self.value_vars:
            arg_info += ArgInfo(name=field + "-" + v, set_func=self.value_vars[v].set, get_func=self.value_vars[v].get)

        return arg_info


class CheckButton(BaseCheckButton):
    def __init__(self,
                 options: str or Tuple[str] or List[Tuple[str, bool]],
                 bind_func=None,
                 name=None,
                 title="请选择",
                 style="primary",
                 tab_index=0,
                 async_run=False,
                 concurrency_mode=ConcurrencyModeFlag.SAFE_CONCURRENCY_MODE_FLAG):
        super().__init__(options=options,
                         bind_func=bind_func,
                         name=name,
                         title=title,
                         style=style,
                         button_style="TCheckbutton",
                         tab_index=tab_index,
                         async_run=async_run,
                         concurrency_mode=concurrency_mode)


class CheckToolButton(BaseCheckButton):
    def __init__(self,
                 options: str or Tuple[str] or List[Tuple[str, bool]],
                 bind_func=None,
                 name=None,
                 title="请选择",
                 style="info",
                 tab_index=0,
                 async_run=False,
                 concurrency_mode=ConcurrencyModeFlag.SAFE_CONCURRENCY_MODE_FLAG):
        super().__init__(options=options,
                         bind_func=bind_func,
                         name=name,
                         title=title,
                         style=style,
                         button_style="Toolbutton",
                         tab_index=tab_index,
                         async_run=async_run,
                         concurrency_mode=concurrency_mode,
                         mode="ToolButton")


class CheckObviousToolButton(BaseCheckButton):
    def __init__(self,
                 options: str or Tuple[str] or List[Tuple[str, bool]],
                 bind_func=None,
                 name=None,
                 title="请选择",
                 style="primary",
                 tab_index=0,
                 async_run=False,
                 concurrency_mode=ConcurrencyModeFlag.SAFE_CONCURRENCY_MODE_FLAG):
        super().__init__(options=options,
                         bind_func=bind_func,
                         name=name,
                         title=title,
                         style=style,
                         button_style="Outline.Toolbutton",
                         tab_index=tab_index,
                         async_run=async_run,
                         concurrency_mode=concurrency_mode,
                         mode="ToolButton")


class ToggleButton(BaseCheckButton):
    def __init__(self,
                 options: str or Tuple[str],
                 bind_func=None,
                 name=None,
                 title="请选择",
                 style="primary",
                 tab_index=0,
                 async_run=False,
                 concurrency_mode=ConcurrencyModeFlag.SAFE_CONCURRENCY_MODE_FLAG):
        assert not isinstance(options, list), "开关按钮仅有开和关两个选项，请传入单个选项"
        super().__init__(options=options,
                         bind_func=bind_func,
                         name=name,
                         title=title,
                         style=style,
                         button_style="Roundtoggle.Toolbutton",
                         tab_index=tab_index,
                         async_run=async_run,
                         concurrency_mode=concurrency_mode)


class BaseRadioButton(BaseNotebookTool):
    def __init__(self,
                 options: str or List[str],
                 default: str = None,
                 bind_func=None,
                 name=None,
                 title="请选择",
                 style="primary",
                 button_style="TRadiobutton",
                 tab_index=0,
                 async_run=False,
                 concurrency_mode=ConcurrencyModeFlag.SAFE_CONCURRENCY_MODE_FLAG,
                 mode=None):
        super().__init__(bind_func=bind_func,
                         name=name,
                         style=style,
                         tab_index=tab_index,
                         async_run=async_run,
                         concurrency_mode=concurrency_mode)
        self.title = title
        self.mode = mode
        self.options = [options] if isinstance(options, str) else options
        self.default = default if default else options[0]
        self.button_style = button_style

    def build(self, *args, **kwargs):
        super().build(*args, **kwargs)
        frame = ttk.Frame(self.master, style="TFrame")

        frame.pack(side="top", fill="x", padx=5, pady=5)
        label = ttk.Label(frame,
                          text=self.title,
                          style="TLabel",
                          width=LABEL_WIDTH)
        label.pack(side="left")

        self.value_var = tkinter.StringVar(frame, value=self.options[0])
        for option in self.options:
            if self.mode == "ToolButton":
                pad_x = 0
            else:
                pad_x = 5
            ttk.Radiobutton(frame,
                            text=option,
                            style=self.style + self.button_style,
                            variable=self.value_var,
                            value=option,
                            command=self._callback(self.bind_func)).pack(side="left", padx=pad_x)

    def get_arg_info(self) -> ArgInfo:
        field = self.name if self.name else self.__class__.__name__
        arg_info = ArgInfo(name=field, set_func=self.value_var.set, get_func=self.value_var.get)

        return arg_info


class RadioButton(BaseRadioButton):
    def __init__(self,
                 options: str or List[str],
                 default: str = None,
                 bind_func=None,
                 name=None,
                 title="请选择",
                 style="primary",
                 tab_index=0,
                 async_run=False,
                 concurrency_mode=ConcurrencyModeFlag.SAFE_CONCURRENCY_MODE_FLAG):
        super().__init__(options=options,
                         default=default,
                         bind_func=bind_func,
                         name=name,
                         title=title,
                         style=style,
                         button_style="TRadiobutton",
                         tab_index=tab_index,
                         async_run=async_run,
                         concurrency_mode=concurrency_mode,
                         mode=None)


class RadioToolButton(BaseRadioButton):
    def __init__(self,
                 options: str or List[str],
                 default: str = None,
                 bind_func=None,
                 name=None,
                 title="请选择",
                 style="info",
                 tab_index=0,
                 async_run=False,
                 concurrency_mode=ConcurrencyModeFlag.SAFE_CONCURRENCY_MODE_FLAG):
        super().__init__(options=options,
                         default=default,
                         bind_func=bind_func,
                         name=name,
                         title=title,
                         style=style,
                         button_style="Toolbutton",
                         tab_index=tab_index,
                         async_run=async_run,
                         concurrency_mode=concurrency_mode,
                         mode="ToolButton")


class RadioObviousToolButton(BaseRadioButton):
    def __init__(self,
                 options: str or List[str],
                 default: str = None,
                 bind_func=None,
                 name=None,
                 title="请选择",
                 style="primary",
                 tab_index=0,
                 async_run=False,
                 concurrency_mode=ConcurrencyModeFlag.SAFE_CONCURRENCY_MODE_FLAG):
        super().__init__(options=options,
                         default=default,
                         bind_func=bind_func,
                         name=name,
                         title=title,
                         style=style,
                         button_style="Outline.Toolbutton",
                         tab_index=tab_index,
                         async_run=async_run,
                         concurrency_mode=concurrency_mode,
                         mode="ToolButton")


class Progressbar(BaseNotebookTool):
    def __init__(self,
                 title: str = "进度条",
                 default: int = 0,
                 max_size: int = 100,
                 name: str = None,
                 style: str = "primary",
                 tab_index: int = 0,
                 async_run: bool = False,
                 concurrency_mode=ConcurrencyModeFlag.SAFE_CONCURRENCY_MODE_FLAG):
        super().__init__(name=name,
                         style=style,
                         tab_index=tab_index,
                         async_run=async_run,
                         concurrency_mode=concurrency_mode)
        self.title = title
        self.default_value = default
        self.max_size = max_size

    def progressbar_var_trace(self, *args):
        v = self.progressbar_var.get()
        self.value_var.set(f"进度 {v:.2f}%")

    def build(self, *args, **kwargs):
        super().build(*args, **kwargs)
        frame = ttk.Frame(self.master, style="TFrame")
        self.progressbar_var = tkinter.IntVar(frame, value=self.default_value)
        self.value_var = tkinter.StringVar(frame, value=f"进度 {self.default_value:.2f}%")
        self.progressbar_var.trace("w", self.progressbar_var_trace)
        frame.pack(side="top", fill="x", padx=5, pady=5)
        label = ttk.Label(frame,
                          text=self.title,
                          style="TLabel",
                          width=LABEL_WIDTH)
        label.pack(side="left")

        progressbar = ttk.Progressbar(frame,
                                      variable=self.progressbar_var,
                                      style=self.style + "Striped.Horizontal.TProgressbar")
        progressbar.pack(side="left", fill="x", expand="yes", padx=5, pady=2)

        self.value = ttk.Label(frame,
                               textvariable=self.value_var,
                               style="TLabel",
                               width=LABEL_WIDTH)
        self.value.pack(side="right")
        return frame

    def get_arg_info(self) -> ArgInfo:
        field = self.name if self.name else self.__class__.__name__
        arg_info = ArgInfo(name=field, set_func=self.progressbar_var.set, get_func=self.progressbar_var.get)

        return arg_info


class BaseCombine(BaseNotebookTool):
    def __init__(self,
                 tools: BaseNotebookTool or List[BaseNotebookTool],
                 side=HORIZONTAL,
                 title=None,
                 style: str = None,
                 tab_index: int = None):
        super().__init__(tab_index=tab_index, style=style)
        self.side = "top" if side else "left"
        self.title = title

        self.tools = tools if isinstance(tools, list) else [tools]

        self.tab_index = tab_index if tab_index else self.tools[0].tab_index

        for tool_id in range(len(self.tools)):
            self.tools[tool_id].tab_index = self.tab_index

    def build(self, *args, **kwargs):
        super().build(self, *args, **kwargs)

        style_mode = "TLabelframe" if self.title else "TFrame"
        if self.title:
            frame = ttk.LabelFrame(self.master, style=self.style + style_mode)
        else:
            frame = ttk.Frame(self.master, style=self.style + style_mode)
        frame.pack(anchor=self.n)
        for tool in self.tools:
            kwargs["master"] = frame
            tool.build(*args, **kwargs)


class HorizontalCombine(BaseCombine):
    def __init__(self,
                 tools: BaseNotebookTool or List[BaseNotebookTool],
                 title=None,
                 style: str = None,
                 tab_index: int = 0):
        super().__init__(tools=tools,
                         side=HORIZONTAL,
                         title=title,
                         style=style,
                         tab_index=tab_index)


class VerticalCombine(BaseCombine):
    def __init__(self,
                 tools: BaseNotebookTool or List[BaseNotebookTool],
                 title=None,
                 style: str = None,
                 tab_index: int = 0):
        super().__init__(tools=tools,
                         side=VERTICAL,
                         title=title,
                         style=style,
                         tab_index=tab_index)
