# Author: Acer Zhang
# Datetime: 2021/9/17 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

from setuptools import setup
from setuptools import find_packages

__version__ = "0.1.2"

# python setup.py sdist bdist_wheel
setup(
    name='QGUI',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/QPT-Family/QGUI',
    license='MIT',
    author='GT-ZhangAcer',
    author_email='zhangacer@foxmail.com',
    description='QWebSite',
    install_requires=["ttkbootstrap", "pillow"],
    python_requires='>3.5',
    include_package_data=True,
)
