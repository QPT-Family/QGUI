# Author: Acer Zhang
# Datetime: 2021/9/14 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os
from typing import List
from types import MethodType, FunctionType

import tkinter
from tkinter import ttk

from qgui.case import CollapsingFrame

BLACK = "#24262d"
GRAY = "#535353"
GREEN = "#76b67e"
FONT = "黑体-简"

# ToDo 更换为绝对路径
ICON = "qgui/resources/icon/play_w.png"

TITLE_BG_COLOR = BLACK
L_BOTTOM_FRAME_COLOR_ON = GREEN


# ToDo 主题部分可考虑通过增加warmup来解决

class BaseFrame:
    pass


class BaseLeftTab:
    def __init__(self):
        self.frame = ttk.Frame(style="primary.TFrame")
        self.frame.place(x=0, y=50, width=180, height=470)
        self.tabs = dict()

    def add_about(self,
                  author="未知作者",
                  version="0.0.1",
                  other_info: List[str] = None):
        bus_cf = CollapsingFrame(self.frame)
        bus_cf.pack(fill='x', pady=0)

        bus_frm = ttk.Frame(bus_cf, padding=5)
        bus_frm.columnconfigure(1, weight=1)
        bus_cf.add(bus_frm, title="相关信息", style='secondary.TButton')

        ttk.Label(bus_frm, text=f"Author:\t{author}", style="TLabel").pack(anchor="nw")
        ttk.Label(bus_frm, text=f"Version:\t{version}", style="TLabel").pack(anchor="nw")

        for line in other_info:
            ttk.Label(bus_frm, text=line, style="TLabel").pack(anchor="nw")

    def add_homepage(self, tool):
        btn = ttk.Button(self.frame,
                         text=tool.name,
                         image=tool.name,
                         compound='left',
                         command=tool.bind_func)
        btn.pack(side='left', ipadx=5, ipady=5, padx=0, pady=1)

    def apply_root(self, master):
        self.frame.master = master


class BaseTool:
    def __init__(self,
                 bind_func,
                 name="未命名组件",
                 icon=None,
                 ):
        if not hasattr(bind_func, "__call__"):
            raise f"{__class__.__name__}的bind_func需具备__call__方法，建议在此传入函数或自行构建具备__call__方法的对象。"

        if icon and not os.path.exists(icon):
            raise f"请确认{os.path.abspath(icon)}是否存在"
        elif icon:
            pass
        else:
            icon = ICON
        self.name = name
        self.bind_func = bind_func
        self.icon = icon


class BaseBar:
    def __init__(self,
                 title: str = "QGUI测试程序",
                 style="primary"):
        self.frame = ttk.Frame(style=style + ".TFrame")
        self.frame.place(x=0, y=0, width=940, height=50)
        self.img_info = dict()

        # 占位标题
        black = tkinter.Frame(self.frame,
                              height=10,
                              bg=TITLE_BG_COLOR)
        black.pack(side="right", anchor="se")
        # 主标题
        # ToDo 需要修改bg
        title = tkinter.Label(self.frame,
                              font=(FONT, 30),
                              fg="AliceBlue",
                              bg="#2d3e50",
                              text=title)
        title.pack(side="right", anchor="se", pady=3)

    def add_tool(self, tool: BaseTool):
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
                         command=tool.bind_func)

        btn.pack(side='left', ipadx=5, ipady=5, padx=0, pady=1)

    def apply_root(self, master):
        self.frame.master = master


if __name__ == '__main__':
    from qgui.factory import CreateQGUI

    _bw = CreateQGUI()

    _bb = BaseBar()
    _bt = BaseLeftTab()

    _bb.apply_root(_bw)
    _bt.apply_root(_bw)

    _bb.add_tool(BaseTool(lambda: print(1),
                          icon="/Users/zhanghongji/PycharmProjects/QGUI/qgui/resources/icon/play_w.png"))
    _bb.add_tool(BaseTool(lambda: print(1),
                          name="222",
                          icon="/Users/zhanghongji/PycharmProjects/QGUI/qgui/resources/icon/play_w.png"))

    _bt.add_about(other_info=["QGUI:\thhhh"])
    _bt.add_about(other_info=["QGUI:\thhhh"])
    _bw.mainloop()
