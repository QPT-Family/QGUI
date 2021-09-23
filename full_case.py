import time

from qgui import CreateQGUI
from qgui.bar_tools import BaseBarTool, GitHub
from qgui.notebook_tools import *
from qgui.manager import QStyle, HORIZONTAL

print("小Tips：超参数可以被Print", HORIZONTAL)


def click(args: dict):
    print("你点到我啦~")
    print("你选择的文件是：", args["文件选择"].get())
    print("保存位置修改为XxX", args["保存位置"].set("XxX"))
    for arg, v_fun in args.items():
        print(arg, v_fun.get())

    for i in range(1, 101):
        time.sleep(0.01)
        args["进度条"].set(i)
        if i % 10 == 0:
            print("当前进度", i)


# 创建主界面
q_gui = CreateQGUI(title="一个新应用",  # 界面标题
                   tab_names=["主控制台", "选择按钮"],  # 界面中心部分的分页标题 - 可不填
                   style=QStyle.default)  # 皮肤

# 在界面最上方添加一个按钮，链接到GitHub主页
q_gui.add_banner_tool(GitHub("https://github.com/QPT-Family/QGUI"))
# 要不试试自定义Banner按钮？
q_gui.add_banner_tool(BaseBarTool(click, name="一个新组件"))
# 在主界面部分添加一个文件选择工具吧~
q_gui.add_notebook_tool(ChooseFileTextButton(name="文件选择"))
# 再加个文件夹选择工具
q_gui.add_notebook_tool(ChooseDirTextButton(name="保存位置"))
q_gui.add_notebook_tool(InputBox())
q_gui.add_notebook_tool(Combobox(options=["11111", "21221"]))
q_gui.add_notebook_tool(Slider(default=4))

# 第二页 - 顺便把按钮绑在一起吧~
combine_left = VerticalCombine([CheckButton(options=[("选择1", 0), ("选择2", 1), ("选择3", 0)]),
                                CheckToolButton(options=[("选择1", 0), ("选择2", 1), ("选择3", 0)]),
                                CheckObviousToolButton(options=[("选择1", 0), ("选择2", 1), ("选择3", 0)]),
                                ToggleButton(options=("开", 1))],
                               tab_index=1)
combine_left.n = "w"
q_gui.add_notebook_tool(combine_left)

combine_right = VerticalCombine([RadioButton(["选择1", "选择2", "选择3"], tab_index=1),
                                 RadioToolButton(["选择1", "选择2", "选择3"], tab_index=1),
                                 RadioObviousToolButton(["选择1", "选择2", "选择3"], tab_index=1)])
combine_right.n = "n"
q_gui.add_notebook_tool(combine_right)

# 要不要再添加一个运行按钮？，绑定刚刚创建的函数吧~
q_gui.add_notebook_tool(Progressbar(name="进度条"))
q_gui.add_notebook_tool(RunButton(click))
# 简单加个简介
q_gui.set_navigation_about(author="GT",
                           version="0.0.1",
                           github_url="https://github.com/QPT-Family/QGUI",
                           other_info=["欢迎加入QPT！"])
# 跑起来~
q_gui.run()
