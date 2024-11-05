# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="emlog",
    version="0.4",
    packages=find_packages(),
    install_requires=[],
    entry_points={},
    description="python版本日志组件",
    author="李栋",
    author_email="frankli715@qq.com",
    url="https://github.com/frankli/emlog",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
)