# -*- coding: utf-8 -*-
# @Time: 2024/10/16 18:11
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:


class NerEntity:
    def __init__(self, label: str, name: str, start: int, end: int):
        self._label = label
        self._name = name
        self._start = start
        self._end = end

    @property
    def label(self):
        return self._label

    @property
    def name(self):
        return self._name

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    def __str__(self):
        return ', '.join(f'{key}={value}' for key, value in self.__dict__.items())
