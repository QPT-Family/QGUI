# Author: Acer Zhang
# Datetime: 2021/9/17 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

from setuptools import setup
from setuptools import find_packages

__version__ = "0.6.1"

# python setup.py sdist bdist_wheel
setup(
    name='QGUI',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/QPT-Family/QGUI',
    license='MIT',
    author='GT-ZhangAcer',
    author_email='zhangacer@foxmail.com',
    description='QGUI - 0.1MB超轻量Python GUI框架，用模板来快捷制作深度学习模型推理界面 ',
    install_requires=["ttkbootstrap==0.5.1", "pillow>=8.2.0"],
    python_requires='>3.5',
    include_package_data=True,
)
