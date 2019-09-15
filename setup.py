#!/usr/bin/env python3

from setuptools import setup

author = "lwzm"
name = "fsm-web"

setup(
    name=name,
    version="1.0",
    description="Fsm store jia http",
    author=author,
    author_email="{}@qq.com".format(author),
    keywords="fsm http web store".split(),
    packages=["fsm_web"],
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3",
    ],
)
