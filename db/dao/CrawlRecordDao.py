from db import DBHelper
from entities import Entity


def insert(position, page, name):
    db = DBHelper.Connector().get_connection()
    cursor = db.cursor()
    sql = "insert into crawl_record(position, page,name) VALUES ('{}','{}','{}')".format(position, page, name)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as ex:
        print(ex)
    finally:
        db.close()


def query():
    db = DBHelper.Connector().get_connection()
    cursor = db.cursor()
    sql = "select position,page,name, max(crawl_id) from crawl_record group by crawl_id"
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        if result is not None and len(result) > 0:
            return Entity.CrawlRecord(result[0], result[1], result[2])
    except Exception as ex:
        print(ex)
        return None
    finally:
        db.close()
