# -*- coding: utf-8 -*-
# @Time: 2024/11/5 20:15
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:

from typing import Dict, Union

import shapely
from shapely.geometry import Polygon, MultiPolygon
from geoi_core.model.entity.loi import (
    Loi,
    LoiDataframe,
    FIELD_LOI_NAME,
    FIELD_LOI_ADDRESS,
    FIELD_LOI_CATEGORY)
from geoi_core.model.basic.geo_feature import GeoFeature, GeoFeatureFrame, EPSG_WGS84


class Aoi(Loi):
    """
    Area Of Interest：兴趣面，Loi的子类
    """

    def __init__(self, id, data: Dict, polygon: Union[Polygon, MultiPolygon], crs=EPSG_WGS84, **kwargs):
        super().__init__(data=data, geom=polygon, id=id, crs=crs, **kwargs)

    @classmethod
    def build_aoi(cls, id, name, address, category, polygon_wkt, attrs: Dict, crs=EPSG_WGS84, **kwargs):
        data = {FIELD_LOI_NAME: name, FIELD_LOI_ADDRESS: address, FIELD_LOI_CATEGORY: category}
        if attrs is not None:
            data.update(attrs)
        plg = shapely.from_wkt(polygon_wkt)
        if not isinstance(plg, (Polygon, MultiPolygon)):
            raise ValueError("polgon_wkt不是标准的面")
        return Aoi(id=id, data=data, polygon=plg, crs=crs, **kwargs)


class AoiDataframe(LoiDataframe):
    """
    Aoi的数据表类
    """

    def construct_feature(self, id, polygon: Union[Polygon, MultiPolygon], data: Dict, crs: str = EPSG_WGS84):
        return Aoi(id=id, data=data, polygon=polygon, crs=crs)
