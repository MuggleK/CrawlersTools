# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/8/12 21:00
# @Author  : MuggleK
# @File    : setup.py

from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='CrawlersTools',  # 包名
    version='1.3.4',  # 版本号
    description='Tools for Crawlers',
    long_description=long_description,
    author='MuggleK',
    author_email='peichangchuan@gmail.com',
    url='https://github.com/MuggleK/CrawlersTools',
    install_requires=[
        "auto_mix_prep==0.2.0",
        "DBUtils==1.3",
        "fontTools",
        "httpx",
        "httpx[http2]",
        "loguru",
        "Pillow",
        "PyExecJS",
        "pymongo==3.5.1",
        "PyMySQL==0.9.3",
        "redis==4.1.3",
        "PyYAML==5.3.1",
        "lxml==4.9.1",
        "numpy==1.21.6",
        "Distance==0.1.3"
    ],
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ],
)
