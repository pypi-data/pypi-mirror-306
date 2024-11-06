# -*- coding: utf-8 -*-
# @Time: 2024/10/18 17:58
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:
import logging
from abc import abstractmethod
from typing import (
    List,
    Dict,
)
from shapely import from_geojson
from shapely.geometry.base import BaseGeometry
from geopandas.geodataframe import GeoDataFrame, GeoSeries
from geoi_core.model.basic.geo_abstract import GeoObject, GeoObjectCollection

EPSG_WGS84 = "EPSG:4326"

logger = logging.getLogger(__name__)


class GeoFeature(GeoObject):
    """
    地理要素类，对所有包含空间属性的地理实体的抽象，它的子类需要：
    1、实现required_fields方法，返回当前实体类必须的属性字段
    """

    def __init__(self, data: Dict, geom: BaseGeometry, id, crs: str = EPSG_WGS84, **kwargs):
        self._data = data
        self.__id = id
        self._geom = geom
        self._crs = crs
        self._required_fields = self.required_fields()
        if data is None or not all(v in self._data for v in self.required_fields()):
            raise ValueError(f"必须包含这些字段:{self.required_fields}")

    @abstractmethod
    def required_fields(self) -> List:
        """返回必要字段"""

    @property
    def id(self):
        return self.__id

    @property
    def geom(self):
        return self._geom

    def set_attributes(self, attributes: Dict):
        """
        这是额外字段值
        """
        if attributes is None:
            return
        self._data.update(attributes)

    def get_value(self, col: str):
        if self._data is None or len(self._data) == 0:
            return None
        return self._data[col]

    def buffer(self, distance):
        return self.geom.buffer(distance)

    def intersects(self, other):
        return self.geom.intersects(other.geom)


class GeoFeatureFrame(GeoObjectCollection):
    """
    地理要素集合类，所有包含空间属性的地理实体集合的抽象，它的子类需要：
    1、在__init__构造函数中，定义一个字段的mapping，即xxFeature必有属性和数据源字段的映射
    2、实现construct_feature方法，用来构造xxFeature
    """

    def __init__(self, geo_dataframe: GeoDataFrame, field_mapping: Dict, id_field=None, crs=EPSG_WGS84):
        self.features: Dict[GeoFeature] = {}
        self.field_mapping: Dict = field_mapping
        if id_field is not None:
            if id_field in geo_dataframe.columns:
                # 修改索引列为用户指定字段，保持__geo_dataframe中的id和数据id一致
                geo_dataframe = geo_dataframe.set_index(id_field)
            else:
                raise ValueError(f"字段'{id_field}'不存在")
        else:
            logger.warning("未指定id字段，默认使用临时id")
        self.__geo_dataframe: GeoDataFrame = geo_dataframe
        self.__geo_series: GeoSeries = geo_dataframe.geometry
        self.crs = crs
        self.init_features()

    def init_features(self):
        for feature in self.__geo_dataframe.iterfeatures():
            properties = feature["properties"]
            # 利用地理实体预定义的字段名称，替换数据属性中的key
            for field, field_name in self.field_mapping.items():
                if field != field_name:
                    tmp = properties.pop(field_name)
                    properties[field] = tmp
            id = feature["id"]
            geom = from_geojson(str(feature["geometry"]).replace("'", "\"").replace("(", "[").replace(")", "]"))
            geo_feature = self.construct_feature(id, geom, properties, self.crs)
            self.features[id] = geo_feature

    @abstractmethod
    def construct_feature(self, id, geom: BaseGeometry, data: Dict, crs: str = EPSG_WGS84):
        """通过属性字典构建地理实体对象"""

    def get_object(self, id) -> GeoObject:
        return self.get_feature(id)

    def get_feature(self, id):
        return self.features[id]

    def get_iterfeatures(self):
        for id, feature in self.features.items():
            yield feature

    def env(self):
        return self.__geo_series.total_bounds

    def map_plot(self):
        return self.__geo_dataframe.plot()

    @property
    def geo_dataframe(self):
        return self.__geo_dataframe
