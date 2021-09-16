# Author: Acer Zhang
# Datetime: 2021/9/14 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import sys
import webbrowser
from typing import List

import tkinter
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from qgui.bar_tools import BaseBarTool
from qgui.third_party.collapsing_frame import CollapsingFrame
from qgui.notebook_tools import BaseNotebookTool

BLACK = "#24262d"
GRAY = "#e3e3e3"
GREEN = "#76b67e"
FONT = "黑体-简"

TITLE_BG_COLOR = BLACK


# ToDo 主题部分可考虑通过增加warmup来解决

class _Backbone:
    def __init__(self, f_style="primary"):
        """
        请务必检查self.frame是否做了pack等定位操作，无操作将不会被显示
        :param f_style:
        """
        # 统一用place
        self.style = f_style
        pass

    def apply_root(self, master):
        self.frame = ttk.Frame(master, style=self.style + ".TFrame")


class BaseNavigation(_Backbone):

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
    def apply_root(self, master):
        super(BaseNavigation, self).apply_root(master)
        self.frame.place(x=0, y=50, width=180, height=470)


class BaseNoteBook(_Backbone):
    def __init__(self,
                 style="primary",
                 tab_names: List[str] = None,
                 stout=None):
        super(BaseNoteBook, self).__init__(f_style=style)
        self.tab_names = tab_names
        self.nb_frames = list()
        if not stout:
            stout = sys.stdout
        self.stout = stout

    def add_tool(self, tool: BaseNotebookTool):
        frame = self.nb_frames[tool.tab_index]
        tool.build(frame)

    def apply_root(self, master):
        super(BaseNoteBook, self).apply_root(master)
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

        self.text_area.insert("end", "控制台链接成功")


class BaseBanner(_Backbone):
    def __init__(self,
                 title: str = "QGUI测试程序",
                 style="primary"):
        super(BaseBanner, self).__init__(f_style=style)
        self.img_info = dict()
        self.title = title

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
                         command=tool.bind_func,
                         style=tool.style)

        btn.pack(side="left", ipadx=5, ipady=5, padx=0, pady=1)

    def apply_root(self, master):
        super(BaseBanner, self).apply_root(master)
        self.frame.place(x=0, y=0, width=940, height=50)
        # 占位标题
        black = tkinter.Frame(self.frame,
                              height=10,
                              bg=TITLE_BG_COLOR)
        black.pack(side="right", anchor="se")
        # 主标题
        title = ttk.Label(self.frame,
                          font=(FONT, 30),
                          text=self.title,
                          style=self.style + ".Inverse.TLabel")
        title.pack(side="right", anchor="se", padx=5, pady=3)


if __name__ == '__main__':
    from qgui.factory import CreateQGUI
    from notebook_tools import ChooseFileTextButton, RunButton
    from qgui.bar_tools import RunTool, GitHub

    _bw = CreateQGUI()

    _bb = BaseBanner()
    _bt = BaseNavigation()
    _btab = BaseNoteBook()

    _bb.apply_root(_bw)
    _bt.apply_root(_bw)
    _btab.apply_root(_bw)

    _bb.add_tool(RunTool(lambda: print(1),
                         name="开始运行",
                         icon="/Users/zhanghongji/PycharmProjects/QGUI/qgui/resources/icon/play_w.png"))
    _bb.add_tool(BaseBarTool(lambda: print(1),
                             name="222",
                             icon="/Users/zhanghongji/PycharmProjects/QGUI/qgui/resources/icon/play_w.png"))
    _bb.add_tool(GitHub("https://github.com/QPT-Family/QGUI"))

    _bt.add_info("一一一一一二二二二二三三三三三四四四四四")
    _bt.add_about(other_info=["QGUI:\thhhh"], github_url="www.baidu.com")


    def tmp_cb(text):
        print(text)


    _btab.add_tool(ChooseFileTextButton(tmp_cb))
    _btab.add_tool(ChooseFileTextButton(tmp_cb))
    _btab.add_tool(ChooseFileTextButton(tmp_cb))
    _btab.add_tool(RunButton(lambda: print("RUN")))
    _bw.mainloop()
