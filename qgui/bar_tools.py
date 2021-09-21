# Author: Acer Zhang
# Datetime: 2021/9/16 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import os
import webbrowser

from qgui.manager import ICON_PATH

RUN_ICON = os.path.join(ICON_PATH, "play_w.png")
GITHUB_ICON = os.path.join(ICON_PATH, "github.png")


class BaseBarTool:
    def __init__(self,
                 bind_func,
                 name="未命名组件",
                 icon=None,
                 style="",
                 ):
        if not hasattr(bind_func, "__call__"):
            raise f"{__class__.__name__}的bind_func需具备__call__方法，建议在此传入函数或自行构建具备__call__方法的对象。\n" \
                  f"Example:\n" \
                  f"    def xxx():\n" \
                  f"        Do sth\n" \
                  f"    MakeThisTool(bind_func=xxx)\n" \
                  f"Error example:\n" \
                  f"    def xxx():\n" \
                  f"        Do sth\n" \
                  f"    MakeThisTool(bind_func=xxx())"

        if icon and not os.path.exists(icon):
            raise f"请确认{os.path.abspath(icon)}是否存在"
        if not icon:
            icon = RUN_ICON
        self.name = name
        self.bind_func = bind_func
        self.icon = icon

        if style:
            self.style = style + ".TButton"
        else:
            self.style = "TButton"


class RunTool(BaseBarTool):
    def __init__(self,
                 bind_func,
                 name="开始执行",
                 icon=None,
                 style="success"):
        if not icon:
            icon = RUN_ICON
        super(RunTool, self).__init__(bind_func,
                                      name=name,
                                      icon=icon,
                                      style=style)


class GitHub(BaseBarTool):
    def __init__(self,
                 url,
                 name="在GitHub上查看该项目",
                 style="primary"):
        icon = GITHUB_ICON
        bind_func = self.github_callback
        super().__init__(bind_func,
                         name=name,
                         icon=icon,
                         style=style)
        self.github_url = url

    def github_callback(self, args):
        webbrowser.open_new(self.github_url)
