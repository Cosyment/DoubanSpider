from db import DBHelper
from entities import Entity


def insert(type, position, page, name):
    db = DBHelper.Connector().get_connection()
    cursor = db.cursor()
    sql = "insert into t_crawl_record(type,position, page,name) VALUES ('{}','{}','{}','{}')".format(type, position,
                                                                                                     page,
                                                                                                     name)

    try:
        cursor.execute(sql)
        db.commit()
    except Exception as ex:
        print(ex)
    finally:
        db.close()


def query(type):
    db = DBHelper.Connector().get_connection()
    cursor = db.cursor()
    # 查询最后一条记录
    sql = "select * from t_crawl_record where type = {} order by id desc limit 1".format(type)
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
        if result is not None and len(result) > 0:
            return Entity.CrawlRecord(result[2], result[3], result[4])
    except Exception as ex:
        print(ex)
        return None
    finally:
        db.close()
