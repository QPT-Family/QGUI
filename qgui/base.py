# Author: Acer Zhang
# Datetime: 2021/9/14 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import sys
import webbrowser
import time
from typing import List

import tkinter
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from qgui.bar_tools import BaseBarTool
from qgui.third_party.collapsing_frame import CollapsingFrame
from qgui.notebook_tools import BaseNotebookTool
from qgui.os_tools import StdOutWrapper

BLACK = "#24262d"
GRAY = "#e3e3e3"
GREEN = "#76b67e"
FONT = "黑体-简"

TITLE_BG_COLOR = BLACK


# ToDo 主题部分可考虑通过增加warmup来解决

class _Backbone:
    """
    整个界面的基础，存放共有的变量
    """

    def __init__(self, f_style="primary"):
        """
        请务必检查self.frame是否做了pack等定位操作，无操作将不会被显示
        :param f_style:
        """
        # 统一用place
        self.style = f_style

        # 全局变量
        self.global_info = dict()

    def apply_root(self, master, global_info):
        self.frame = ttk.Frame(master, style=self.style + ".TFrame")
        self.global_info = global_info


class BaseNavigation(_Backbone):
    """
    左侧导航栏基本框架
    """

    def __init__(self, style="primary"):
        super(BaseNavigation, self).__init__(f_style=style)
        self.tabs = dict()

    def add_about(self,
                  author: str = "未知作者",
                  version: str = "0.0.1",
                  github_url: str = None,
                  other_info: List[str] = None):
        bus_cf = CollapsingFrame(self.frame)
        bus_cf.pack(fill='x', pady=0)

        bus_frm = ttk.Frame(bus_cf, padding=5)
        bus_frm.columnconfigure(1, weight=1)
        bus_cf.add(bus_frm, title="相关信息", style='secondary.TButton')

        ttk.Label(bus_frm, text=f"作者:\t{author}", style="TLabel", justify="left").pack(anchor="nw")
        ttk.Label(bus_frm, text=f"版本:\t{version}", style="TLabel", justify="left").pack(anchor="nw")

        if other_info:
            for line in other_info:
                ttk.Label(bus_frm, text=line, style="TLabel").pack(anchor="nw")

        if github_url:
            def github_callback(event):
                webbrowser.open_new(github_url)

            github_label = ttk.Label(bus_frm, text=f"> 进入GitHub", style="info.TLabel", justify="left")
            github_label.pack(anchor="nw")
            github_label.bind("<Button-1>", github_callback)

    def add_info(self,
                 info: str,
                 split_len=15):
        bus_cf = CollapsingFrame(self.frame)
        bus_cf.pack(fill='x', pady=0)

        bus_frm = ttk.Frame(bus_cf, padding=5)
        bus_frm.columnconfigure(1, weight=1)
        bus_cf.add(bus_frm, title="项目简介", style='secondary.TButton', justify="left")

        new_info = str()
        if split_len:
            for row in range(len(info) // split_len):
                new_info += info[row * split_len:(row + 1) * split_len] + "\n"
            else:
                new_info += info[(len(info) // split_len) * split_len:]
        else:
            new_info = info
        ttk.Label(bus_frm, text=new_info, style="TLabel").pack(anchor="nw")

    # def add_homepage(self, tool):
    #     btn = ttk.Button(self.frame,
    #                      text=tool.name,
    #                      image=tool.name,
    #                      compound='left',
    #                      command=tool.bind_func)
    #     btn.pack(side='left', ipadx=5, ipady=5, padx=0, pady=1)
    def apply_root(self, master, global_info):
        super(BaseNavigation, self).apply_root(master, global_info)
        self.frame.place(x=0, y=50, width=180, height=470)


class BaseNoteBook(_Backbone):
    """
    中间Notebook部分框架
    """

    def __init__(self,
                 style="primary",
                 tab_names: List[str] = None,
                 stdout=None):
        super(BaseNoteBook, self).__init__(f_style=style)
        self.tab_names = tab_names
        self.nb_frames = list()
        if not stdout:
            stdout = sys.stdout
        self.stdout = stdout

    def add_tool(self, tool: BaseNotebookTool):
        if tool.tab_index >= len(self.nb_frames):
            raise
        frame = self.nb_frames[tool.tab_index]

        tool_info = tool.get_info()
        if tool_info:
            for info in tool_info:
                if info in self.global_info:
                    self.global_info[info + "-QGUI-" + len(self.global_info)] = tool_info[info]
                else:
                    self.global_info[info] = tool_info[info]
        tool.build(master=frame, global_info=self.global_info)

    def apply_root(self, master, global_info):
        super(BaseNoteBook, self).apply_root(master, global_info)
        self.frame.place(x=182, y=55, width=750, height=460)
        self.nb = ttk.Notebook(self.frame)
        self.nb.pack(side="top", fill="both", expand="yes")

        if self.tab_names:
            for tab_name in self.tab_names:
                sub_frame = ttk.Frame(self.nb)
                sub_frame.pack(anchor="nw", expand="yes")
                self.nb_frames.append(sub_frame)
                self.nb.add(sub_frame, text=tab_name)
        else:
            sub_frame = ttk.Frame(self.nb)
            sub_frame.pack(anchor="nw", expand="yes")
            self.nb_frames.append(sub_frame)
            self.nb.add(sub_frame, text="主程序控制台")

        # 增加OutPut
        self.console_frame = ttk.Frame(self.frame,
                                       style=self.style + ".TFrame")
        self.console_frame.pack(side="top", fill='both')

        # 标题
        self.title = ttk.Label(self.console_frame,
                               font=(FONT, 15),
                               style=self.style + ".Inverse.TLabel",
                               text="控制台日志",
                               justify="left")
        self.title.pack(side="top", fill="x", expand="yes", padx=10, pady=5)

        # 文本
        self.text_area = ScrolledText(self.console_frame,
                                      highlightcolor=master.style.colors.primary,
                                      highlightbackground=master.style.colors.border,
                                      highlightthickness=1)
        self.text_area.pack(fill="both", expand="yes")

        def _write_log_callback(text):
            if text and text != "\n":
                text = time.strftime("%H:%M:%S", time.localtime()) + "\t" + text
            self.text_area.insert("end", text)

        sys.stdout = StdOutWrapper(self.stdout, callback=_write_log_callback)
        self.text_area.insert("end", "控制台链接成功\n")


class BaseBanner(_Backbone):
    def __init__(self,
                 title: str = "QGUI测试程序",
                 style="primary"):
        super(BaseBanner, self).__init__(f_style=style)
        self.img_info = dict()
        self.title = title

    def _callback(self, func):
        def render():
            func(self.global_info)

        return render

    def add_tool(self, tool: BaseBarTool):
        """
        添加小工具组件
        :param
        """

        self.img_info[tool.name] = tkinter.PhotoImage(name=tool.name,
                                                      file=tool.icon)

        btn = ttk.Button(self.frame,
                         text=tool.name,
                         image=tool.name,
                         compound='left',
                         command=self._callback(tool.bind_func),
                         style=tool.style)

        btn.pack(side="left", ipadx=5, ipady=5, padx=0, pady=1)

    def apply_root(self, master, global_info):
        super(BaseBanner, self).apply_root(master, global_info)
        self.frame.place(x=0, y=0, width=940, height=50)
        # 占位标题
        black = tkinter.Frame(self.frame,
                              height=10,
                              bg=TITLE_BG_COLOR)
        black.pack(side="right", anchor="se")
        # 主标题
        title = ttk.Label(self.frame,
                          font=(FONT, 25),
                          text=self.title,
                          style=self.style + ".Inverse.TLabel")
        title.pack(side="right", anchor="se", padx=5, pady=3)


if __name__ == '__main__':
    pass
