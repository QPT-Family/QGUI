# Author: Acer Zhang
# Datetime: 2021/9/14 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import tkinter
from tkinter import ttk

BLACK = "#24262d"
GRAY = "#535353"
GREEN = "#76b67e"

TITLE_BG_COLOR = BLACK
L_BOTTOM_FRAME_COLOR_ON = GREEN


# ToDo 主题部分可考虑通过增加warmup来解决

class BaseWindow:
    def __init__(self):
        self.main_tk = tkinter.Tk()
        self.main_tk.geometry("840x500")

    def get_master(self):
        return self.main_tk


class BaseFrame:
    pass


class BaseTab:
    def __init__(self):
        self.frame = tkinter.Frame(bg=GRAY, width=150)
        self.frame.pack(fill="y", anchor="nw")
        # self.frame.pack_propagate(False)
        self.tabs = dict()
        self.add_frame(BaseFrame())

    def add_frame(self,
                  frame: BaseFrame,
                  subtitle="测试标题",
                  subtitle_icon=None):
        # ToDo 加icon的功能
        button_frame = tkinter.Frame(self.frame,
                                     height=50,
                                     width=150,
                                     bg=GRAY)
        button_frame.grid()
        # button_frame.grid_propagate(False)
        l_bottom_frame = tkinter.Frame(button_frame,
                                       width=10,
                                       height=50,
                                       bg=L_BOTTOM_FRAME_COLOR_ON)
        l_bottom_frame.pack(fill="y", side="top", expand=True)
        button = tkinter.Button(button_frame,
                                bd=0,
                                height=10,
                                bg=GRAY)
        button.pack(fill="y", side="top", expand=True)

    def apply_root(self, master):
        self.frame.master = master


class BaseBanner:
    def __init__(self, title: str = "QGUI测试程序"):
        self.frame = tkinter.Frame(bg=TITLE_BG_COLOR)
        self.frame.pack(fill="x", anchor="nw")
        self._set_title(title)

    def _set_title(self, text):
        # 占位标题
        black = tkinter.Frame(self.frame,
                              height=5,
                              bg=TITLE_BG_COLOR)
        black.grid(row=0)
        # 主标题
        title = tkinter.Label(self.frame,
                              font=("等线", 30),
                              fg="AliceBlue",
                              bg=TITLE_BG_COLOR,
                              text=text,
                              anchor="sw",
                              height=1)
        title.grid(sticky="sw", row=1, padx=5, pady=3)

    def apply_root(self, master):
        self.frame.master = master


if __name__ == '__main__':
    _bw = BaseWindow()
    _bw.get_master().wm_resizable(False, False)

    _bb = BaseBanner()
    _bt = BaseTab()

    _bb.apply_root(_bw.get_master())
    _bt.apply_root(_bw.get_master())

    _bw.get_master().mainloop()
