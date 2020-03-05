from db import DBHelper


def insert( name, cover, rating, year, director, writer, actors, type, release_date, duration,
           introduction,
           trailer_url):
    db = DBHelper.Connector().get_connection()
    cursor = db.cursor()
    name = name.replace("\'", "\\'")
    director = director.replace("\'", "\\'")
    actors = actors.replace("\'", "\\'")
    introduction = introduction.replace("\"", "\\\"").replace("\'", "\\'")
    sql = "insert into movie(name, cover,rating,year, director, writer, actors, type, release_date, duration, introduction, trailer) " \
          "values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(name, cover, rating,
                                                                                        year,
                                                                                        director,
                                                                                        writer,
                                                                                        actors, type,
                                                                                        release_date,
                                                                                        duration,
                                                                                        introduction,
                                                                                        trailer_url)
    query_sql = "select name from movie where name='{}'".format(name)
    try:
        # 执行sql语句
        cursor.execute(query_sql)
        # 提交到数据库执行
        result = cursor.fetchall()
        if len(result) == 0:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            print("----------->>>>数据插入成功")
        else:
            print("----------->>>>数据表中记录已存在")
    except Exception as ex:
        print(ex)
        # 如果发生错误则回滚
        db.rollback()
    # 关闭数据库连接
    db.close()
