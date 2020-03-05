from functools import wraps

import pymysql.cursors


def singleton(cls):
    instance = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return get_instance


# 数据库连接实例
@singleton
class Connector(object):
    connection = None
    host = ''  # mysql主机地址
    user = ''  # mysql用户名
    pwd = ''  # mysql密码
    db = ''  # mysql数据库

    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.pwd = "root"
        self.db = "imovie"

    def get_connection(self):
        try:
            return pymysql.connect(self.host, self.user, self.pwd, self.db)
        except Exception as ex:
            print(ex)
