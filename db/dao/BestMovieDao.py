from db import DBHelper


def insert(ranking, title, cover, rating, year, director, writer, actors, type, release_date, duration,
           introduction,
           trailer_url):
    db = DBHelper.Connector().get_connection()
    cursor = db.cursor()
    title = title.replace("\'", "\\'")
    director = director.replace("\'", "\\'")
    actors = actors.replace("\'", "\\'")
    introduction = introduction.replace("\"", "\\\"").replace("\'", "\\'")
    sql = "insert into t_movie(title, cover,rating,year, director, writer, actors, type, release_date, duration, introduction, trailer,ranking) " \
          "values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(title, cover, rating,
                                                                                             year,
                                                                                             director,
                                                                                             writer,
                                                                                             actors, type,
                                                                                             release_date,
                                                                                             duration,
                                                                                             introduction,
                                                                                             trailer_url,
                                                                                             ranking)
    query_sql = "select t.title from t_movie t where t.title=\'{}'".format(title)
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
            update_sql = "UPDATE t_movie t SET t.ranking = \'{}' WHERE t.title =\'{}'".format(ranking, title)
            cursor.execute(update_sql)
            db.commit()
            print("----------->>>>更新经典电影信息 《{}》，豆瓣排名 {}".format(title, ranking))
    except Exception as ex:
        print(ex)
        # 如果发生错误则回滚
        db.rollback()
    # 关闭数据库连接
    db.close()
