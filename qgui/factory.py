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
from qgui.notebook_tools import BaseFrameTool


class CreateQGUI:
    def __init__(self,
                 title="未命名应用",
                 style=QStyle.default,
                 banner: BaseBanner = None,
                 navigation: BaseNavigation = None,
                 notebook: BaseNoteBook = None):
        super().__init__()
        self.title = title
        self.style = style

        self.root = tkinter.Tk(title)
        if self.style:
            self.root.style = Style(self.style)
        else:
            self.root.style = Style()
        self.root.style.configure('bg.TFrame', background=self.root.style.colors.inputbg)
        self.root.style.configure('bg.TLabel', background=self.root.style.colors.inputbg)
        self.root.geometry("940x520")
        self.root.wm_resizable(False, False)

        # 初始化组件
        self.banner = banner if banner else BaseBanner(title=self.title)
        self.navigation = navigation if navigation else BaseNavigation()
        self.notebook = notebook if notebook else BaseNoteBook()

        self.banner.apply_root(self.root)
        self.navigation.apply_root(self.root)
        self.notebook.apply_root(self.root)

    def add_banner_tool(self, tool: BaseBarTool):
        self.banner.add_tool(tool)

    def add_notebook_tool(self, tool: BaseFrameTool):
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
                            info: str,
                            split_len=15):
        self.navigation.add_info(info=info,
                                 split_len=split_len)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    from qgui.bar_tools import BaseBarTool
    from qgui.notebook_tools import ChooseFileTextButton

    _tmp = CreateQGUI()
    _tmp.add_banner_tool(BaseBarTool(lambda: print(0)))
    _tmp.add_notebook_tool(ChooseFileTextButton(lambda: print(1)))
    _tmp.set_navigation_about()
    _tmp.run()
