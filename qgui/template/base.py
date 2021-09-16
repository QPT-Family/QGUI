from qgui.factory import CreateQGUI
from qgui.bar_tools import BaseBarTool
from qgui.notebook_tools import ChooseFileTextButton, RunButton


def click(*args):
    print("你点到我啦~", args)


# 创建主界面
main_gui = CreateQGUI(title="一个新应用")

# 在界面最上方添加一个按钮，并绑定刚刚创建的click()函数
main_gui.add_banner_tool(BaseBarTool(click))
# 在主界面部分添加一个文件选择工具，也绑定刚刚的函数吧~
main_gui.add_notebook_tool(ChooseFileTextButton(click))
# 要不要再添加一个运行按钮？
main_gui.add_notebook_tool(RunButton(click))
# 简单加个简介
main_gui.set_navigation_about(author="GT",
                              version="0.0.1",
                              github_url="https://github.com/QPT-Family/QGUI",
                              other_info=["欢迎加入QPT！"])
# 跑起来~
main_gui.run()
