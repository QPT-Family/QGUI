# Author: Acer Zhang
# Datetime: 2021/9/14 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os

import qgui

QGUI_BASE_PATH = os.path.dirname(qgui.__file__)
RESOURCES_PATH = os.path.join(QGUI_BASE_PATH, "resources")
ICON_PATH = os.path.join(RESOURCES_PATH, "icon")


class QStyle:
    default = None
    lumen= "lumen"
    # 以下需后期重新定制颜色方案
    paddle = "cosmo"
