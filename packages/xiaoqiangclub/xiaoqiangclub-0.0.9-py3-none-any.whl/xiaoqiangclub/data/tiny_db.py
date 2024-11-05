# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/1 17:52
# 文件名称： tiny_db.py
# 项目描述： tinydb模块封装
# 开发工具： PyCharm
import os
from tinydb import TinyDB, Query
from typing import List, Dict, Union, Optional
from xiaoqiangclub.config.log_config import log


class TinyDBManager:
    def __init__(self, db_file: str = 'tiny_db.json') -> None:
        """
        tinydb 封装：https://tinydb.readthedocs.io/en/latest/index.html
        :param db_file: 数据库文件名，默认为'tiny_db.json'
        """
        log.debug(f"初始化 TinyDBManager，数据库文件: {db_file}")
        db_file = db_file.strip('.json') + '.json'
        self.db_file = db_file
        self.db = TinyDB(db_file)
        self.search = self.query  # 查询

    def insert(self, data: Union[Dict, List[Dict]], table_name: str = 'default',
               skip_existing: bool = False) -> Optional[Union[str, List[str]]]:
        """
        向指定表中插入数据

        :param data: 要插入的数据，可以是单个字典或字典列表（用于批量插入）
        :param table_name: 表名，默认为'default'
        :param skip_existing: 是否跳过已存在的数据
        :return: 插入操作的文档 ID 列表
        """
        try:
            table = self.db.table(table_name)
            if isinstance(data, list):
                items_to_insert = []
                for item in data:
                    if skip_existing and self._exists(item, table):
                        log.debug(f"数据已存在，跳过插入: {item}")
                        continue
                    items_to_insert.append(item)
                return table.insert_multiple(items_to_insert)
            else:
                if skip_existing and self._exists(data, table):
                    log.debug(f"数据已存在，跳过插入: {data}")
                    return []
                return table.insert(data)
        except Exception as e:
            log.error(f"插入数据时出现错误 (表: {table_name}, 数据: {data}): {repr(e)}")
            return None

    def _exists(self, data: Dict, table: TinyDB) -> bool:
        """
        检查数据是否已存在于表中

        :param data: 要检查的字典数据
        :param table: TinyDB 表对象
        :return: 如果存在返回 True，否则返回 False
        """
        conditions = [getattr(Query(), key) == value for key, value in data.items()]
        combined_condition = self._combine_conditions(conditions)
        return table.search(combined_condition) != []

    def query(self, conditions: Dict, table_name: str = 'default', is_global: bool = False) -> Optional[List[Dict]]:
        """
        查询表中符合条件的数据

        :param conditions: 查询条件字典
        :param table_name: 表名，默认为'default'
        :param is_global: 是否查询整个数据库，默认为False，表示只查询指定表。当is_global为True时，table_name 将被忽略。
        :return: 符合条件的字典列表
        """
        log.debug(f"查询表 {table_name}，查询条件: {conditions}, 查询范围: {'整个数据库' if is_global else '指定表'}")
        try:
            if is_global:
                # 查询整个数据库
                results = []
                for table_name in self.db.tables():
                    table = self.db.table(table_name)
                    conditions_list = [getattr(Query(), key) == value for key, value in conditions.items()]
                    combined_condition = self._combine_conditions(conditions_list)
                    result = table.search(combined_condition)
                    results.extend(result)
                log.debug(f"查询结果: {results}")
                return results
            else:
                # 查询指定表
                table = self.db.table(table_name)
                conditions_list = [getattr(Query(), key) == value for key, value in conditions.items()]
                combined_condition = self._combine_conditions(conditions_list)
                result = table.search(combined_condition)
                log.debug(f"查询结果: {result}")
                return result
        except Exception as e:
            log.error(f"查询数据时出现错误: {repr(e)}")
            return None

    def update(self, query: Dict, new_data: Union[Dict, List[Dict]], table_name: str = 'default') -> Optional[
        List[int]]:
        """
        更新符合条件的数据

        :param query: 查询条件字典
        :param new_data: 新的数据字典或字典列表
        :param table_name: 表名，默认为'default'
        :return: 更新操作影响的文档 ID 列表
        """
        log.debug(f"更新表 {table_name}，查询条件: {query}，新的数据: {new_data}")
        try:
            table = self.db.table(table_name)
            conditions_list = [getattr(Query(), key) == value for key, value in query.items()]
            combined_condition = self._combine_conditions(conditions_list)
            if isinstance(new_data, dict):
                result = table.update(new_data, combined_condition)
            elif isinstance(new_data, list):
                updates = [(data, combined_condition) for data in new_data]
                result = table.update_multiple(updates)
            else:
                raise ValueError("不支持的 new_data 类型")
            log.debug(f"更新成功，返回被更新的文档 ID: {result}")
            return result
        except Exception as e:
            log.error(f"更新数据时出现错误: {repr(e)}")
            return None

    def delete(self, query: Dict = None, table_name: str = 'default', delete_table: bool = False,
               delete_file: bool = False) -> None:
        """
        删除符合条件的数据或删除整个表或数据库文件

        :param query: 查询条件字典
        :param table_name: 表名，默认为'default'
        :param delete_table: 是否删除整个表
        :param delete_file: 是否删除数据库文件
        """
        log.debug(f"删除操作，表: {table_name}, 查询条件: {query}, 删除表: {delete_table}, 删除文件: {delete_file}")
        try:
            if delete_file:
                os.remove(self.db_file)
                log.debug(f"删除数据库文件: {self.db_file}")
                return
            elif delete_table:
                self.db.drop_table(table_name)
                log.debug(f"删除表: {table_name}")
                return
            else:
                table = self.db.table(table_name)
                if query:
                    conditions_list = [getattr(Query(), key) == value for key, value in query.items()]
                    combined_condition = self._combine_conditions(conditions_list)
                    table.remove(combined_condition)
                    log.debug(f"删除符合条件的记录: {query}")
                else:
                    raise ValueError("如果不删除表或文件，必须提供查询条件用于删除数据")
        except Exception as e:
            log.error(f"删除操作时出现错误: {repr(e)}")

    def close(self) -> None:
        """
        关闭数据库连接
        """
        log.debug("关闭数据库连接...")
        try:
            self.db.close()
        except Exception as e:
            log.error(f"关闭数据库连接时出现错误: {repr(e)}")

    @staticmethod
    def _combine_conditions(conditions: List) -> Optional[Query]:
        if not conditions:
            return None
        combined_condition = conditions[0]
        for condition in conditions[1:]:
            combined_condition &= condition
        return combined_condition
