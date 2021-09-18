from qgui import CreateQGUI
from qgui.bar_tools import BaseBarTool, GitHub
from qgui.notebook_tools import ChooseFileTextButton, RunButton, ChooseDirTextButton, InputBox, Combobox


def click(args: dict):
    print("你点到我啦~")
    for arg, v_fun in args.items():
        print(arg, v_fun())


# 创建主界面
main_gui = CreateQGUI(title="一个新应用")

# 在界面最上方添加一个按钮，链接到GitHub主页
main_gui.add_banner_tool(GitHub("https://github.com/QPT-Family/QGUI"))
# 要不试试自定义Banner按钮？
main_gui.add_banner_tool(BaseBarTool(click, name="一个新组件"))
# 在主界面部分添加一个文件选择工具吧~
main_gui.add_notebook_tool(ChooseFileTextButton(name="文件选择"))
# 再加个文件夹选择工具
main_gui.add_notebook_tool(ChooseDirTextButton(name="保存位置"))
main_gui.add_notebook_tool(InputBox())
main_gui.add_notebook_tool(Combobox(options=["11111", "21221"]))
# 要不要再添加一个运行按钮？，绑定刚刚创建的函数吧~
main_gui.add_notebook_tool(RunButton(click))
# 简单加个简介
main_gui.set_navigation_about(author="GT",
                              version="0.0.1",
                              github_url="https://github.com/QPT-Family/QGUI",
                              other_info=["欢迎加入QPT！"])
# 跑起来~
main_gui.run()
