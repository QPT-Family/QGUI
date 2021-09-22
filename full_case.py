from qgui import CreateQGUI
from qgui.bar_tools import BaseBarTool, GitHub
from qgui.notebook_tools import *
from qgui.manager import QStyle


def click(args: dict):
    print("你点到我啦~")
    print("你选择的文件是：", args["文件选择"].get())
    print("保存位置修改为XxX", args["保存位置"].set("XxX"))
    for arg, v_fun in args.items():
        print(arg, v_fun.get())


# 创建主界面
main_gui = CreateQGUI(title="一个新应用", tab_names=["主控制台", "选择按钮"])

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
main_gui.add_notebook_tool(Slider(default=4))
# 第二页
main_gui.add_notebook_tool(CheckButton(options=[("选择1", 0), ("选择2", 1), ("选择3", 0)], tab_index=1))
main_gui.add_notebook_tool(CheckToolButton(options=[("选择1", 0), ("选择2", 1), ("选择3", 0)], tab_index=1))
main_gui.add_notebook_tool(CheckObviousToolButton(options=[("选择1", 0), ("选择2", 1), ("选择3", 0)], tab_index=1))
main_gui.add_notebook_tool(ToggleButton(options=("开", 1), tab_index=1))

main_gui.add_notebook_tool(RadioButton(["选择1", "选择2", "选择3"], tab_index=1))
main_gui.add_notebook_tool(RadioToolButton(["选择1", "选择2", "选择3"], tab_index=1))
main_gui.add_notebook_tool(RadioObviousToolButton(["选择1", "选择2", "选择3"], tab_index=1))

# 要不要再添加一个运行按钮？，绑定刚刚创建的函数吧~
main_gui.add_notebook_tool(RunButton(click))
# 简单加个简介
main_gui.set_navigation_about(author="GT",
                              version="0.0.1",
                              github_url="https://github.com/QPT-Family/QGUI",
                              other_info=["欢迎加入QPT！"])
# 跑起来~
main_gui.run()
