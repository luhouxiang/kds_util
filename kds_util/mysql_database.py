"""
@author: luhx
@describe: 数据库的封装
@example:
db_config = {'db_host':'xxx', 'db_port':xxx, 'db_user': 'xxx', 'db_pass': 'xxx', 'db_database': 'xxx'}
# 注意: db_port: 为整型，如3306
mysql = MySQL(db_config)
mysql.query(sql)
"""
import pymysql

from .user_logbook import user_log as logger
from typing import Dict


class MySQL:
    # 在这里配置自己的SQL服务器
    def __init__(self, db_config: Dict[str, str]):
        self.__config = db_config
        self.__db = None
        self.db_host = self.__config['db_host']
        self.db_port = self.__config['db_port']
        self.db_user = self.__config['db_user']
        self.db_pass = self.__config['db_pass']
        self.db_database = self.__config['db_database']
        self.db_status = "fail"
        self.__connect()

    def __del__(self):
        if self.__db is not None:
            self.__db.close()

    def __connect(self):
        if self.__db is None:
            try:
                self.__db = pymysql.connect(
                    host=self.db_host,
                    port=self.db_port,
                    user=self.db_user,
                    passwd=self.db_pass,
                    db=self.db_database,
                    charset="utf8"
                )
            except Exception as e:
                logger.info(e)
                print(e)
            self.db_status = "success" if self.__db is not None else "fail"
        return self.__db

    def query(self, _sql):
        cursor = self.__connect().cursor()
        try:
            cursor.execute(_sql)
            data = cursor.fetchall()
            # 提交到数据库执行
            self.__connect().commit()
        except Exception as e:
            print(e)
            logger.info("error:{}:{}".format(e, _sql))
            # 如果发生错误则回滚
            self.__connect().rollback()
            return []
        return data

    def insert(self, sql):
        cursor = self.__connect().cursor()
        try:
            cursor.execute(sql)
            insert_id = self.__connect().insert_id()
            # 提交到数据库执行
            self.__connect().commit()
        except Exception as e:
            print(e)
            logger.info("error:{}:{}".format(e, sql))
            # 如果发生错误则回滚
            self.__connect().rollback()
            return False, 0
        return True, insert_id

    def delete(self, sql) -> int:
        """
        返回>=0表示执行成功后受影响的行数，否则返回-1
        """
        cursor = self.__connect().cursor()
        try:
            rel = cursor.execute(sql)
            # 提交到数据库执行
            self.__connect().commit()
        except Exception as e:
            print(e)
            logger.info("error:{}:{}".format(e, sql))
            rel = -1
            # 如果发生错误则回滚
            self.__connect().rollback()
        return rel

    def exec(self, sql):
        cursor = self.__connect().cursor()
        try:
            cursor.execute(sql)
            # 提交到数据库执行
            self.__connect().commit()
        except Exception as e:
            print(e)
            logger.info("error:{}:{}".format(e, sql))
            # 如果发生错误则回滚
            self.__connect().rollback()
            return False
        return True

    def exec_many(self, _sql_list):
        cursor = self.__connect().cursor()
        try:
            if len(_sql_list) == 0:
                return True
            for sql in _sql_list:
                cursor.execute(sql)
            self.__connect().commit()
        except Exception as e:
            print(e)
            logger.info("error:{}:{}".format(e, _sql_list))
            # 如果发生错误则回滚
            self.__connect().rollback()
            return False
        return True


class PyMySql(MySQL):
    def __init__(self, pymysql_url: str = "mysql+pymysql://root:2234567@192.168.1.100:3306/hqdb?charset=utf8"):
        # config = {}
        # pos = pymysql_url.find("://")
        # b = pymysql_url[pos+3:]
        # user_pass = b.split("@")[0]
        # c = b.split("@")[1]
        # host_port = c.split("/")[0]
        # db_utf = c.split("/")[1]
        # config['db_host'] = host_port.split(":")[0]
        # config['db_port'] = int(host_port.split(":")[1])
        # config['db_user'] = user_pass.split(":")[0]
        # config['db_pass'] = user_pass.split(":")[1]
        # config['db_database'] = db_utf.split("?")[0]
        config = {}
        pos = pymysql_url.find("://")
        b = pymysql_url[pos + 3:]
        pos2 = b.rfind("@")
        user_pass = b[:pos2]
        ip_all = b[pos2 + 1:]
        host_port = ip_all.split("/")[0]
        db_utf = ip_all.split("/")[1]
        config['db_host'] = host_port.split(":")[0]
        config['db_port'] = int(host_port.split(":")[1])
        config['db_user'] = user_pass.split(":")[0]
        config['db_pass'] = user_pass.split(":")[1]
        config['db_database'] = db_utf.split("?")[0]
        MySQL.__init__(self, config)
