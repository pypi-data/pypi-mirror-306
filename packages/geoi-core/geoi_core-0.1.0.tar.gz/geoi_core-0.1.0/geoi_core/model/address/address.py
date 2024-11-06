# -*- coding: utf-8 -*-
# @Time: 2024/10/14 12:33
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:

from address_ner import NerEntity
from typing import List, Optional

DISTRICT_LABELS = ["Province", "City", "County", "Town", "Village"]
FUNCTION_LABELS = ["Residence", "School", "Institution", "Road", "RoadNum", "RoadAux", "Location"]
BUILDING_LABELS = ["Build", "BuildNum"]
ROOM_LABELS = ["Room"]


class AddressElement(object):
    """
    地址元素类，是构成一个完整地址Address的子元素，相当于地址链上的节点
    """

    def __init__(self, address: str, name: str, start: int, end: int, label: str):
        self._ori_address = address
        self._name = name
        self._start = start
        self._end = end
        self._label = label.strip("")
        self._level = -1
        self._child = None
        self._parent = None
        self._full_address = None
        self.__init_level()
        self.__init_full_address()

    def __init_level(self):
        if self._label in DISTRICT_LABELS:
            self._level = 1
        elif self._label in FUNCTION_LABELS:
            self._level = 2
        elif self._label in BUILDING_LABELS:
            self._level = 3
        elif self._label in ROOM_LABELS:
            self._level = 4

    def __init_full_address(self):
        self._full_address = self._ori_address[0:self._end + 1]

    def get_sub_address(self):
        """返回子地址集合"""
        sub_lst = []
        if self.is_leaf:
            return self._name
        next_elem: AddressElement = self._child
        while next_elem:
            sub_lst.append(next_elem.name)
            next_elem = next_elem.child

    def get_sub_address_group_level(self):
        """返回基于level级别的子地址集合"""
        sub_lst = []
        group = []
        cur_level = self._level
        if self.is_leaf:
            return self._name
        next_elem: AddressElement = self._child
        group.append(self._name)
        while next_elem:
            if next_elem.level == cur_level:
                group.append(next_elem.name)
            else:
                sub_lst.append(''.join(group))
                group.clear()
                group.append(next_elem.name)

            sub_lst.append(next_elem.name)
            next_elem = next_elem.child
            cur_level = next_elem.level

    @property
    def parent(self) -> 'AddressElement':
        return self._parent

    @parent.setter
    def parent(self, parent):
        if self._parent is None:
            self._parent = parent
        else:
            raise AttributeError("赋值后不能修改")

    @property
    def child(self) -> 'AddressElement':
        return self._child

    @child.setter
    def child(self, child):
        if self._child is None:
            self._child = child
        else:
            raise AttributeError("赋值后不能修改")

    @property
    def name(self):
        return self._name

    @property
    def level(self):
        return self._level

    @property
    def ori_address(self):
        return self._ori_address

    @property
    def full_address(self):
        return self._full_address

    @property
    def label(self):
        return self._label

    @property
    def is_root(self):
        return self._parent is None

    @property
    def is_leaf(self):
        return self._child is None


class Address:
    """
    标准地址类，代表由多个AddressElement元素构成的地址元素链，且必须是按层级由小到大的属性
    """

    def __init__(self, address: str, root_elem: AddressElement = None):
        self._ori_address = address  # 原始地址文本
        self._root_elem = root_elem
        self._leaf_elem = None
        self._aux_addresses: List[Address]  # 一个长地址文本中可能有多条地址链，
        self._sub_elements: List = [None, [], [], [], []]  # 初始化每个级别的空数组，方便进行标准化的读取,0位永远为空
        self._elem_address: str  # 所有地址元素拼接的地址
        self.__init_sub_elements()

    def __init_sub_elements(self):
        """
        初始化级别数组_sub_elements、叶子元素_leaf_elem
        TODO:如果此时_root_elem还没有构建完会出现问题
        """
        if self._root_elem is None:
            return
        cur_elem: AddressElement = self._root_elem
        cur_level = self._root_elem.level
        cur_level_group = self._sub_elements[cur_level]
        while cur_elem:
            if cur_elem.level == cur_level:
                cur_level_group.append(cur_elem)
            elif cur_elem.level > cur_level:
                cur_level = cur_elem.level
                cur_level_group = self._sub_elements[cur_level]
                cur_level_group.append(cur_elem)
            else:
                raise RuntimeError("地址元素级别颠倒")
            if cur_elem.child is None:
                self._leaf_elem = cur_elem
            cur_elem = cur_elem.child
        # 构造_elem_address
        elem_name_array = []
        for i in range(1, len(self._sub_elements)):
            for elem in self._sub_elements[i]:
                e: AddressElement = elem
                elem_name_array.append(e.name)
        self._elem_address = ''.join(elem_name_array)

    @classmethod
    def ner(cls, address_str: str):
        """

        Args:
            address_str ():

        Returns:

        """
        # do ner
        return address_str

    @classmethod
    def build_address_by_ner_result(cls, address_str: str, ner_entities: List[NerEntity]) -> Optional['Address']:
        """
        基于ner结果构造Address对象（一个地址文本中有多个地址链会进行聚合，只返回主地址，其他地址可通过aux_addresses获取）
        Args:
            address_str (str):原始地址
            ner_entities (List[NerEntity]):ner处理后的结果

        Returns:
            原始地址中提取的地址
        """
        address = None
        addresses = Address.flat_build_address_by_ner_result(address_str, ner_entities)
        if len(addresses) > 0:
            address = Address.integrate_address(addresses)
        return address

    @classmethod
    def flat_build_address_by_ner_result(cls, address_str: str, ner_entities: List[NerEntity]) -> List['Address']:
        """
        基于ner结果构造Address对象（因为一个地址中可能有多个地址链，所以结果为集合）
        TODO:同一个level内部的规则
        Args:
            address_str (str):原始地址
            ner_entities (List[NerEntity]):ner处理后的结果

        Returns:
            原始地址中提取的所有地址链
        """
        if ner_entities is None or len(ner_entities) == 0:
            return []
        addresses = []
        # 处理为json可以识别的标准格式
        # line_ner = ner_res.replace("'", "\"").replace("[(", "[").replace(")]", "]")
        # dic_label_to_elem = json.loads(line_ner)
        ner_entities.sort(key=lambda n: n.start)
        root: AddressElement = None
        pre = None
        cur_level = -1
        for ner_entity in ner_entities:
            # 按顺序构建elem，并初始化对应链路
            addr_elem = AddressElement(address_str, ner_entity.name, ner_entity.start, ner_entity.end, ner_entity.label)
            if addr_elem.level < cur_level:
                # 目前地址元素的level比当前level小，则上一个地址链构造完了，构造一个Address并添加
                addresses.append(Address(root.ori_address, root))
                root = addr_elem
                pre = addr_elem
                cur_level = addr_elem.level
                continue
            addr_elem.parent = pre
            if pre is None:
                root = addr_elem
            else:
                pre.child = addr_elem
            pre = addr_elem
            cur_level = addr_elem.level
        # 最后一个地址链构建完（要等地址链构建完再构建Address否则初始化不完整）
        addresses.append(Address(root.ori_address, root))
        return addresses

    @staticmethod
    def integrate_address(addresses: List['Address']) -> Optional['Address']:
        if addresses is None or len(addresses) == 0:
            return None
        # 暂时以第一个为主地址，剩下的为辅助地址
        base_address = addresses[0]
        if len(addresses) > 1:
            base_address.aux_addresses = addresses[1:len(addresses)]
        return base_address

    @property
    def leaf_elem(self):
        return self._leaf_elem

    @property
    def root_elem(self):
        return self._root_elem

    @property
    def ori_address(self):
        return self._ori_address

    @property
    def elem_address(self):
        return self._elem_address

    @property
    def aux_addresses(self):
        return self._aux_addresses

    @aux_addresses.setter
    def aux_addresses(self, aux_addresses):
        self._aux_addresses = aux_addresses

    def get_level_elems(self, level: int) -> List[AddressElement]:
        """
        获取某个级别所有的地址元素
        Args:
            level (int): 级别

        Returns:
            当前级别所有元素列表
        """
        if level < 1 or level > 4:
            raise ValueError("错误的level")
        if level < self._root_elem.level:
            raise ValueError("level应大于" + str(self._root_elem.level))
        if level > self._leaf_elem.level:
            raise ValueError("level应小于" + str(self._leaf_elem.level))
        if self._sub_elements is not None:
            return self._sub_elements[level]

    def get_level_first_elem(self, level: int) -> AddressElement:
        """
        获取指定级别中的第一个元素
        Args:
            level (int): 级别

        Returns:
            指定级别第一个元素
        """
        level_group = self.get_level_elems(level)
        return level_group[0]

    def get_level_string(self, level: int) -> str:
        """
        获取某个级别的完整名称
        Args:
            level (int): 级别

        Returns:
            当前级别按顺序拼接好的名称字符串
        """
        level_group = self.get_level_elems(level)
        if level_group is None:
            return ''
        level_str = ''.join([_.name for _ in level_group])
        return level_str
