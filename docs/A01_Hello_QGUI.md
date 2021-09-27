# Hello QGUI - 创建一个最简单的QGUI程序


```python
from qgui import CreateQGUI
from qgui.notebook_tools import RunButton


def click(args):
    print("Hello QGUI, 你点到我啦~")


# 创建主界面
q_gui = CreateQGUI(title="一个新应用")

# 添加运行按钮，并绑定click函数，当点击该按钮时将被会触发
q_gui.add_notebook_tool(RunButton(bind_func=click))

# 跑起来~
q_gui.run()
```