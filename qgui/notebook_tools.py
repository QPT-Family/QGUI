# Author: Acer Zhang
# Datetime: 2021/9/16 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

from typing import List, Dict, Tuple
from collections import OrderedDict

import tkinter
from tkinter import ttk
from tkinter import filedialog

from qgui.manager import *
from qgui.base_tools import ConcurrencyModeFlag, check_callable, ArgInfo, select_var_dtype, BaseTool, make_anchor

RUN_ICON = os.path.join(ICON_PATH, "play_w.png")

LEFT_PAD_LEN = 10
LABEL_WIDTH = 12
INPUT_BOX_LEN = 70
DEFAULT_PAD = 5


class BaseNotebookTool(BaseTool):
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
        super().__init__(bind_func=bind_func,
                         name=name,
                         style=style,
                         async_run=async_run,
                         concurrency_mode=concurrency_mode)
        self.tab_index = tab_index


class BaseChooseFileTextButton(BaseNotebookTool):
    def __init__(self,
                 bind_func=None,
                 name: str = None,
                 label_info: str = "目标文件路径",
                 entry_info: str = "请选择文件路径",
                 button_info: str = "选 择 文 件 ",
                 style: str = "primary",
                 tab_index: int = 0,
                 async_run: bool = False,
                 mode="file"):
        super().__init__(bind_func, name=name, style=style, tab_index=tab_index, async_run=async_run)

        self.label_info = label_info
        self.button_info = button_info
        self.name = name
        self.mode = mode

        self.entry_var = tkinter.StringVar(value=entry_info)

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

        if self.mode == "file":
            if not hasattr(self, "filetypes"):
                self.filetypes = [('All Files', '*')]

            def render():
                file_path = filedialog.askopenfilename(title="选择文件",
                                                       filetypes=self.filetypes)
                if file_path:
                    self.entry_var.set(file_path)

        else:
            def render():
                file_path = filedialog.askdirectory(title="选择文件夹")
                if file_path:
                    self.entry_var.set(file_path)

        command = self._callback(self.bind_func, start_func=render) if self.bind_func else render
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
                         async_run=async_run,
                         mode="dir")


class BaseButton(BaseNotebookTool):
    def __init__(self,
                 bind_func,
                 name: str = None,
                 text: str = "开始执行",
                 icon: str = None,
                 checked_text: str = None,
                 async_run: bool = True,
                 style: str = "primary",
                 tab_index: int = 0,
                 concurrency_mode: bool = False,
                 add_width=8):
        super().__init__(bind_func,
                         name=name,
                         style=style,
                         tab_index=tab_index,
                         async_run=async_run,
                         concurrency_mode=concurrency_mode)
        self.text = text
        self.checked_text = checked_text
        self.add_width = add_width

        self.icon = icon

    def build(self, **kwargs) -> tkinter.Frame:
        super().build(**kwargs)
        frame = ttk.Frame(self.master, style="TFrame")
        frame.pack(side="top", fill="x", padx=5, pady=5)
        if self.icon:
            self.icon = tkinter.PhotoImage(file=self.icon)
        else:
            self.icon = None

        self.text_var = tkinter.StringVar(frame, value=self.text)

        def click_btn():
            self.btn.configure(style=self.style + "TButton")
            self.btn.configure(state="disable")
            if self.checked_text:
                self.text_var.set(self.checked_text)

        def done_btn():
            self.btn.configure(style=self.style + "TButton")
            self.btn.configure(state="normal")
            self.text_var.set(self.text)

        self.btn = ttk.Button(frame,
                              textvariable=self.text_var,
                              image=self.icon,
                              width=len(self.text) + self.add_width,
                              compound='left',
                              command=self._callback(self.bind_func, click_btn, done_btn),
                              style=self.style + "TButton")

        self.btn.pack(anchor="ne", padx=0, pady=0)
        return frame


class RunButton(BaseButton):
    def __init__(self,
                 bind_func,
                 name: str = None,
                 text: str = "开始执行",
                 checked_text: str = "正在执行",
                 async_run: bool = True,
                 style: str = "success",
                 tab_index: int = 0,
                 concurrency_mode: bool = False):
        super().__init__(bind_func=bind_func,
                         name=name,
                         text=text,
                         checked_text=checked_text,
                         async_run=async_run,
                         style=style,
                         tab_index=tab_index,
                         concurrency_mode=concurrency_mode,
                         add_width=6,
                         icon=RUN_ICON)


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
        if self.bind_func:
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
                               variable=self.slider_var)
        # ToDo ttk 的Bug
        # self.scale.configure(style="info.TSlider")
        self.scale.pack(side="left", padx=5, fill="x", expand="yes")
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
        return frame

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
        return frame

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
        frame.pack(side="top", fill="x", padx=5, pady=5, expand="yes")
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
                 title: str = None,
                 text: str = None,
                 style: str = None,
                 tab_index: int = None):
        super().__init__(tab_index=tab_index, style=style)
        self.side = "top" if side == HORIZONTAL else "left"
        self.title = title
        self.text = text

        self.tools = tools if isinstance(tools, list) else [tools]

        self.tab_index = tab_index if tab_index else self.tools[0].tab_index

        for tool_id in range(len(self.tools)):
            self.tools[tool_id].tab_index = self.tab_index

    def get_arg_info(self) -> ArgInfo:
        local_info = ArgInfo()
        for tool_id in range(len(self.tools)):
            local_info += self.tools[tool_id].get_arg_info()
        return local_info


class BaseFrameCombine(BaseCombine):
    def build(self, *args, **kwargs):
        super().build(self, *args, **kwargs)

        style_mode = "TLabelframe" if self.title else "TFrame"
        if self.title:
            frame = ttk.LabelFrame(self.master, text=self.title, style=self.style + style_mode)
        else:
            frame = ttk.Frame(self.master, text=self.title, style=self.style + style_mode)
        frame.pack(side="left", anchor="nw", fill="both", expand="yes", padx=8, pady=8)
        if self.text:
            label = ttk.Label(frame,
                              text=self.text,
                              style="TLabel")
            label.pack(side="top", anchor="nw", padx=5)
        for tool in self.tools:
            kwargs["master"] = frame
            tool.build(*args, **kwargs)
        return frame


class HorizontalFrameCombine(BaseFrameCombine):
    def __init__(self,
                 tools: BaseNotebookTool or List[BaseNotebookTool],
                 title=None,
                 style: str = None,
                 text: str = None,
                 tab_index: int = 0):
        super().__init__(tools=tools,
                         side=HORIZONTAL,
                         title=title,
                         style=style,
                         text=text,
                         tab_index=tab_index)


class VerticalFrameCombine(BaseFrameCombine):
    def __init__(self,
                 tools: BaseNotebookTool or List[BaseNotebookTool],
                 title=None,
                 style: str = None,
                 text: str = None,
                 tab_index: int = 0):
        super().__init__(tools=tools,
                         side=VERTICAL,
                         title=title,
                         style=style,
                         text=text,
                         tab_index=tab_index)


class HorizontalToolsCombine(BaseCombine):
    def __init__(self,
                 tools: BaseNotebookTool or List[BaseNotebookTool],
                 title=None,
                 style: str = None,
                 text: str = None,
                 tab_index: int = None):
        super().__init__(tools=tools,
                         side=HORIZONTAL,
                         title=title,
                         style=style,
                         text=text,
                         tab_index=tab_index)

    def build(self, *args, **kwargs):
        super().build(self, *args, **kwargs)
        style_mode = "TLabelframe" if self.title else "TFrame"
        if self.title:
            frame = ttk.LabelFrame(self.master, text=self.title, style=self.style + style_mode)
        else:
            frame = ttk.Frame(self.master, style=self.style + style_mode)
        frame.pack(side="top", fill="x", expand="yes")
        if self.text:
            label = ttk.Label(frame,
                              text=self.text,
                              style="TLabel")
            label.pack(side="top", anchor="nw", padx=5)
        for tool in self.tools:
            sub_frame = ttk.Frame(frame, style="TFrame")
            sub_frame.pack(side="left", fill="x", expand="yes")
            kwargs["master"] = sub_frame
            tool.build(*args, **kwargs)
        return frame


class Label(BaseNotebookTool):
    def __init__(self,
                 name: str = None,
                 text: str = None,
                 title:str=None,
                 alignment: str = LEFT + TOP,
                 style: str = "primary",
                 tab_index: int = 0):
        super(Label, self).__init__(name=name,
                                    style=style,
                                    tab_index=tab_index)
        self.text = text
        self.title = title
        self.alignment = alignment

        self.label_var = tkinter.StringVar(value=self.text)

    def build(self, *args, **kwargs) -> tkinter.Frame:
        super(Label, self).build(*args, **kwargs)
        frame = ttk.Frame(self.master)
        frame.pack(side="top", fill="both", padx=DEFAULT_PAD, pady=DEFAULT_PAD)
        title = ttk.Label(frame,
                          text=self.title,
                          style="TLabel",
                          width=LABEL_WIDTH)
        title.pack(side="left")

        label = ttk.Label(frame,
                          text=self.text,
                          textvariable=self.label_var,
                          style="TLabel")
        # make_anchor(self.alignment)
        label.pack(anchor=make_anchor(self.alignment))
        return frame

    def get_arg_info(self) -> ArgInfo:
        field = self.name if self.name else self.__class__.__name__
        local_info = ArgInfo(field, set_func=self.label_var.set, get_func=self.label_var.get)
        return local_info
