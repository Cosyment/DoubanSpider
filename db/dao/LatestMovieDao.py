from db import DBHelper


def insert(title, alias, language, cover, rating, year, director, writer, actors, type, release_date, area, duration,
           introduction,
           trailer_url):
    db = DBHelper.Connector().get_connection()
    cursor = db.cursor()
    title = title.replace("\'", "\\'")
    director = director.replace("\'", "\\'")
    actors = actors.replace("\'", "\\'")
    introduction = introduction.replace("\"", "\\\"").replace("\'", "\\'")
    sql = "insert into t_movie(title,alias,language, cover,rating,year, director, writer, actors, type, release_date,area, duration, introduction, trailer,latest) " \
          "values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(title,
                                                                                                            alias,
                                                                                                            language,
                                                                                                            cover,
                                                                                                            rating,
                                                                                                            year,
                                                                                                            director,
                                                                                                            writer,
                                                                                                            actors,
                                                                                                            type,
                                                                                                            release_date,
                                                                                                            area,
                                                                                                            duration,
                                                                                                            introduction,
                                                                                                            trailer_url,
                                                                                                            1)
    query_sql = "select title from t_movie where title=\'{}'".format(title)
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
            # update_sql = "UPDATE t_movie t SET t.latest = 1 WHERE t.title =\'{}'".format(title)
            update_sql = "UPDATE t_movie t SET t.latest = 1,t.alias=\'{}',t.area=\'{}',t.writer=\'{}',t.language=\'{}' WHERE t.title =\'{}'".format(
                alias, area, writer, language, title)
            cursor.execute(update_sql)
            db.commit()
            print("----------->>>>更新最新电影信息 《{}》".format(title))
    except Exception as ex:
        print(ex)
        # 如果发生错误则回滚
        db.rollback()
    # 关闭数据库连接
    db.close()
