# -*- coding: utf-8 -*-
# @Time: 2024/10/18 17:58
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:


import logging
import geopandas as gpd
import pandas as pd
from typing import Dict
from geopandas.geodataframe import GeoDataFrame
from shapely.geometry import Point
from geoi_core.model.entity.loi import (
    Loi,
    LoiDataframe,
    FIELD_LOI_ID,
    FIELD_LOI_NAME,
    FIELD_LOI_ADDRESS,
    FIELD_LOI_CATEGORY)
from geoi_core.model.basic.geo_feature import GeoFeature, GeoFeatureFrame, EPSG_WGS84

logger = logging.getLogger(__name__)

FIELD_POI_LNG = "lng"
FIELD_POI_LAT = "lat"


class Poi(Loi):
    """
    Point Of Interest：兴趣面，Poi的子类
    """

    def __init__(self, id, data: Dict, point: Point, crs=EPSG_WGS84, **kwargs):
        super().__init__(data=data, geom=point, id=id, crs=crs, **kwargs)

    @classmethod
    def build_poi(cls, id, name, address, category, lng, lat, attrs: Dict, crs=EPSG_WGS84, **kwargs):
        data = {FIELD_LOI_NAME: name, FIELD_LOI_ADDRESS: address, FIELD_LOI_CATEGORY: category}
        if attrs is not None:
            data.update(attrs)
        return Poi(id=id, data=data, point=Point(lng, lat), crs=crs, **kwargs)


class PoiDataframe(LoiDataframe):
    """
    poi的数据表类，一种poi的集合，既可以通过id访问某一个poi，也可以对整体进行查询、筛选等操作
    """

    def construct_feature(self, id, point: Point, data: Dict, crs: str = EPSG_WGS84):
        return Poi(id=id, data=data, point=point, crs=crs)


def read_poi_csv_xy(poi_csv_path: str, lng_field=FIELD_POI_LNG, lat_field=FIELD_POI_LAT, id_field=FIELD_LOI_ID,
                    name_field=FIELD_LOI_NAME,
                    address_field=FIELD_LOI_ADDRESS,
                    category_field=FIELD_LOI_CATEGORY, encoding="utf-8") -> PoiDataframe:
    dataframe = gpd.read_file(poi_csv_path, encoding=encoding)
    # 从lng、lat转为points
    dataframe[[lng_field, lat_field]] = dataframe[[lng_field, lat_field]].apply(pd.to_numeric)
    geo_dataframe = GeoDataFrame(dataframe, geometry=gpd.points_from_xy(dataframe[lng_field], dataframe[lat_field]))
    return PoiDataframe(geo_dataframe=geo_dataframe, id_field=id_field, name_field=name_field,
                        address_field=address_field,
                        category_field=category_field)
