# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/8/12 21:00
# @Author  : MuggleK
# @File    : setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='CrawlersTools',  # 包名
    version='1.4.78',  # 版本号
    description='Tools for Crawlers',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='MuggleK',
    author_email='peichangchuan@gmail.com',
    url='https://github.com/MuggleK/CrawlersTools',
    install_requires=[
        "auto_mix_prep",
        "DBUtils==1.3",
        "fontTools",
        "httpx",
        "httpx[http2]",
        "loguru",
        "Pillow",
        "PyExecJS==1.5.1",
        "pymongo",
        "PyMySQL",
        "redis",
        "tqdm",
        "PyYAML",
        "lxml",
        "numpy",
        "Distance",
        "chardet",
        "sinan",
        "kafka-python"
    ],
    license='BSD License',
    packages=find_packages(where='.', exclude=(), include=('*',)),
    platforms=["all"],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ],
)
