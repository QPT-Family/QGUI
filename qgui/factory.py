# Author: Acer Zhang
# Datetime: 2021/8/31 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
from typing import List

import tkinter
from ttkbootstrap import Style

from qgui.manager import QStyle
from qgui.base import BaseNoteBook, BaseBanner, BaseNavigation
from qgui.bar_tools import BaseBarTool
from qgui.notebook_tools import BaseNotebookTool


class CreateQGUI:
    def __init__(self,
                 title="未命名应用",
                 style=QStyle.default,
                 stout=None,
                 tab_names: List[str] = None,
                 banner: BaseBanner = None,
                 navigation: BaseNavigation = None,
                 notebook: BaseNoteBook = None):
        super().__init__()
        self.title = title
        self.style = style

        self.root = tkinter.Tk()
        if self.style:
            self.root.style = Style(self.style)
        else:
            self.root.style = Style()
        self.root.style.configure('bg.TFrame', background=self.root.style.colors.inputbg)
        self.root.style.configure('bg.TLabel', background=self.root.style.colors.inputbg)
        self.root.geometry("940x520")
        self.root.wm_resizable(False, False)
        self.root.title(self.title)

        # 初始化组件
        self.banner = banner if banner else BaseBanner(title=self.title)
        self.navigation = navigation if navigation else BaseNavigation()
        self.notebook = notebook if notebook else BaseNoteBook(tab_names=tab_names, stdout=stout)

        # ToDo 做个 global_info管理器，目前信息只从Notebook中流出
        self.banner.apply_root(self.root, self.notebook.global_info)
        self.navigation.apply_root(self.root, self.notebook.global_info)
        self.notebook.apply_root(self.root, self.notebook.global_info)

    def add_banner_tool(self, tool: BaseBarTool):
        self.banner.add_tool(tool)

    def add_notebook_tool(self, tool: BaseNotebookTool):
        self.notebook.add_tool(tool)

    def set_navigation_about(self,
                             author: str = "未知作者",
                             version: str = "0.0.1",
                             github_url: str = None,
                             other_info: List[str] = None):
        self.navigation.add_about(author=author,
                                  version=version,
                                  github_url=github_url,
                                  other_info=other_info)

    def set_navigation_info(self,
                            info: str):
        self.navigation.add_info(info=info)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    from qgui.bar_tools import BaseBarTool
    from qgui.notebook_tools import BaseChooseFileTextButton

    _tmp = CreateQGUI()
    _tmp.add_banner_tool(BaseBarTool(lambda: print(0)))
    _tmp.add_notebook_tool(BaseChooseFileTextButton(lambda: print(1)))
    _tmp.set_navigation_about()
    _tmp.run()
