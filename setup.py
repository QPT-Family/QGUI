# Author: Acer Zhang
# Datetime: 2021/9/17 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

from setuptools import setup
from setuptools import find_packages
from qgui import __version__

# python setup.py sdist bdist_wheel
setup(
    name='QWebSite',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/QPT-Family/QGUI',
    license='MIT',
    author='GT-ZhangAcer',
    author_email='zhangacer@foxmail.com',
    description='QWebSite',
    install_requires=["ttkbootstrap"],
    python_requires='>3.5',
    include_package_data=True,
)