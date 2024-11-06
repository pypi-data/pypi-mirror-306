# -*- coding: utf-8 -*-
# @Time: 2024/11/5 20:18
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc: Location Of Interest

import logging
import geopandas as gpd
from geopandas.geodataframe import GeoDataFrame
from typing import List, Dict

import shapely

from shapely.geometry.base import BaseGeometry

from geoi_core.model.basic.geo_feature import GeoFeature, GeoFeatureFrame, EPSG_WGS84

logger = logging.getLogger(__name__)

FIELD_LOI_ID = "id"
FIELD_LOI_NAME = "name"
FIELD_LOI_ADDRESS = "address"
FIELD_LOI_CATEGORY = "category"
FIELD_LOI_GEOM = "geom"


class Loi(GeoFeature):
    """
    Location Of Interest：兴趣位置，可能是点、面或者线甚至几何集合
    """

    def __init__(self, id, data: Dict, geom: BaseGeometry, crs=EPSG_WGS84, **kwargs):
        super().__init__(data=data, geom=geom, id=id, crs=crs, **kwargs)

    @classmethod
    def build_loi(cls, id, name, address, category, wkt, attrs: Dict, crs=EPSG_WGS84, **kwargs):
        data = {FIELD_LOI_NAME: name, FIELD_LOI_ADDRESS: address, FIELD_LOI_CATEGORY: category}
        if attrs is not None:
            data.update(attrs)
        return Loi(id=id, data=data, point=shapely.from_wkt(wkt), crs=crs, **kwargs)

    @property
    def name(self) -> str:
        return self.get_value(FIELD_LOI_NAME)

    @property
    def address(self) -> str:
        return self.get_value(FIELD_LOI_ADDRESS)

    @property
    def category(self) -> str:
        return self.get_value(FIELD_LOI_CATEGORY)

    def required_fields(self) -> List:
        return [FIELD_LOI_NAME, FIELD_LOI_ADDRESS, FIELD_LOI_CATEGORY]

    def exact_same(self, loi, tolerance=0.00001) -> bool:
        """
        精确匹配，名称和地址完全一致，空间位置在tolerance之内一致
        """
        return (self.name == loi.name and
                self.address == loi.address and
                self.geom.equals_exact(loi.geom, tolerance))

    def same(self, loi, tolerance=0.00001) -> bool:
        """
        一般匹配，名称+地址结合判断实体一致性为exact_match且分数在0.6以上，空间位置在tolerance之内一致
        """
        from geoi_core.model.similarity import mgeo_model
        inputs = (f"{self.address}{self.name}", f"{loi.address}{loi.name}")
        result = mgeo_model.predict(inputs)
        return result[0] == "exact_match" and result[1] > 0.6 and self.geom.equals_exact(loi.geom, tolerance)


class LoiDataframe(GeoFeatureFrame):
    """
    loi的数据表类，一种loi的集合，既可以通过id访问某一个loi，也可以对整体进行查询、筛选等操作
    """

    def __init__(self, geo_dataframe: GeoDataFrame, name_field=FIELD_LOI_NAME, address_field=FIELD_LOI_ADDRESS,
                 category_field=FIELD_LOI_CATEGORY, id_field=FIELD_LOI_ID, crs=EPSG_WGS84):
        field_mappings = {FIELD_LOI_NAME: name_field, FIELD_LOI_ADDRESS: address_field,
                          FIELD_LOI_CATEGORY: category_field}
        super().__init__(geo_dataframe=geo_dataframe, field_mapping=field_mappings, id_field=id_field, crs=crs)

    def construct_feature(self, id, geom: BaseGeometry, data: Dict, crs: str = EPSG_WGS84):
        return Loi(id=id, data=data, geom=geom, crs=crs)


def read_loi_shp(loi_shp_path: str, id_field=FIELD_LOI_ID, name_field=FIELD_LOI_NAME, address_field=FIELD_LOI_ADDRESS,
                 category_field=FIELD_LOI_CATEGORY, encoding="utf-8") -> LoiDataframe:
    dataframe = gpd.read_file(loi_shp_path, encoding=encoding)
    return LoiDataframe(geo_dataframe=dataframe, id_field=id_field, name_field=name_field, address_field=address_field,
                        category_field=category_field)


def read_loi_csv_wkt(poi_csv_path: str, geom_field=FIELD_LOI_GEOM, id_field=FIELD_LOI_ID, name_field=FIELD_LOI_NAME,
                     address_field=FIELD_LOI_ADDRESS,
                     category_field=FIELD_LOI_CATEGORY, encoding="utf-8") -> LoiDataframe:
    dataframe = gpd.read_file(poi_csv_path, encoding=encoding)
    # 从wkt转为几何对象
    dataframe[geom_field] = dataframe[geom_field].apply(shapely.from_wkt)
    geo_dataframe = GeoDataFrame(dataframe, geometry=geom_field)
    return LoiDataframe(geo_dataframe=geo_dataframe, id_field=id_field, name_field=name_field,
                        address_field=address_field,
                        category_field=category_field)
