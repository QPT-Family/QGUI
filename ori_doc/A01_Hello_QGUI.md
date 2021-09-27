# Hello QGUI - 创建一个最简单的QGUI程序

## 简介

在本文中我们讲会创建一个最基础的QGUI对象，当然第一次使用QGUI的你肯定会有很多疑惑，或许以下内容可以帮到你，不妨试试看吧~

### 相关链接

组件类 - A类文档
> [xxx]()

功能类 - B类文档

## 简单示例

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

## API说明

### CreateQGUI
```python
from qgui import CreateQGUI, QStyle

CreateQGUI(
    title="未命名应用",
    style=QStyle.default,
    stout=None,
    tab_names=None,
    banner=None,
    navigation=None,
    notebook=None,
    bind_func=None
)
"""
    创建最基础的QGUI程序
    
    :param title: 主程序标题
    :param style: 皮肤，需通过QStyle来确定
    Example QStyle.paddle
    
    :param stout: 标准输出流
    Example sys.stdout
    
    :param tab_names: List[str] 功能区Tab页面，默认为“主程序控制台”
    Example ["主程序控制台", "控制台2"]
    
    :param banner: QGUI的Banner对象
    :param navigation: QGUI的navigation对象
    :param notebook: QGUI的notebook对象
    :param bind_func: 全局事件绑定
"""
```
#### add_banner_tool
```python
def add_banner_tool(self, tool: BaseBarTool):
    """
    在程序最上方添加小组件
    :param tool: 继承于BaseBarTool的组件对象
    Example
        from qgui.banner_tools import GitHub
        q_gui = CreateQGUI()
        q_gui.add_banner_tool(GitHub())
    """
```
#### add_notebook_tool
```python
def add_notebook_tool(self, tool: BaseNotebookTool):
    """
    在程序中央功能区添加小组件
    :param tool: 继承于BaseNotebookTool的组件对象
    Example
        from qgui.notebook_tools import RunButton
        q_gui.add_notebook_tool(RunButton())
    """
```
#### set_navigation_about
```python
def set_navigation_about(self,
                         author: str = "未知作者",
                         version: str = "0.0.1",
                         github_url: str = None,
                         other_info: List[str] = None):
    """
    设置左侧导航栏的程序基本信息
    :param author: 作者
    :param version: 版本号
    :param github_url: GitHub链接
    """
```
