# -*- coding: utf-8 -*-
# @Time: 2024/10/21 14:14
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:
from abc import abstractmethod


class GeoObject:
    """
    地理要素顶级抽象类
    """

    @abstractmethod
    def geom(self):
        """返回当前对象的几何信息"""


class GeoObjectCollection:
    """
    地理要素集合顶级抽象类
    """

    @abstractmethod
    def get_object(self, id) -> GeoObject:
        """根据id获取地理对象"""
