# -*- coding: utf-8 -*-
# @Time: 2024/11/6 11:09
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:
from setuptools import setup, find_packages

setup(
    name="geoi_core",
    version="0.1.1",
    author="JUST",
    author_email="suiyuan@jd.com",
    description="basic geographic models for intelligent application",
    long_description=open('readme.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="http://xingyun.jd.com/codingRoot/geo_intelligence/geoi_core/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
