from db import DBHelper


def insert(title, cover, rating, year, director, writer, actors, type, release_date, duration,
           introduction,
           trailer_url):
    db = DBHelper.Connector().get_connection()
    cursor = db.cursor()
    title = title.replace("\'", "\\'")
    director = director.replace("\'", "\\'")
    actors = actors.replace("\'", "\\'")
    introduction = introduction.replace("\"", "\\\"").replace("\'", "\\'")

    sql = "insert into t_movie(title, cover,rating,year, director, writer, actors, type, release_date, duration, introduction, trailer) " \
          "values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(title, cover, rating,
                                                                                        year,
                                                                                        director,
                                                                                        writer,
                                                                                        actors, type,
                                                                                        release_date,
                                                                                        duration,
                                                                                        introduction,
                                                                                        trailer_url)
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
            print("----------->>>>数据表中记录已存在")
    except Exception as ex:
        print(ex)
        # 如果发生错误则回滚
        db.rollback()
    # 关闭数据库连接
    db.close()


# 根据电影名称查找
def searchByName(name):
    # 打开数据库连接
    db = DBHelper.Connector().get_connection()
    # 获取游标
    cursor = db.cursor()
    # SQL 查询语句
    sql = "select * from t_movie where title like '%{}%'".format(name)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()  # 获取查询内容
        print("搜索结果有{}个".format(len(result)))
        index = 1
        for i in result:
            print("\nIndex:{}".format(index))
            print("豆瓣链接：{}".format(i[10]))
            print("片名：{}".format(i[0]))
            print("导演：{}".format(i[1]))
            print("编剧：{}".format(i[2]))
            print("主演：{}".format(i[3]))
            print("类型：{}".format(i[4]))
            print("上映日期：{}".format(i[5]))
            print("片长：{}".format(i[6]))
            print("IMDb：{}".format(i[7]))
            print("简介：\n{}".format(i[8]))
            print("预告片链接：{}".format(i[9]))
            index += 1
        print()
    except:
        print("数据查询异常")
        db.rollback()  # 回滚
    db.close()  # 关闭数据库连接


# 查询函数2
def searchByType(name):
    # 打开数据库连接
    db = DBHelper.Connector().get_connection()
    # 获取游标
    cursor = db.cursor()
    # SQL 查询语句
    sql = "select * from t_movie where type like '%{}%'".format(name)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()  # 获取查询内容
        print("搜索结果有{}个".format(len(result)))
        index = 1
        for i in result:
            print("\nIndex:{}".format(index))
            print("豆瓣链接：{}".format(i[10]))
            print("片名：{}".format(i[0]))
            print("导演：{}".format(i[1]))
            print("编剧：{}".format(i[2]))
            print("主演：{}".format(i[3]))
            print("类型：{}".format(i[4]))
            print("上映日期：{}".format(i[5]))
            print("片长：{}".format(i[6]))
            print("IMDb：{}".format(i[7]))
            print("简介：\n{}".format(i[8]))
            print("预告片链接：{}".format(i[9]))
            index += 1
        print()
    except:
        db.rollback()
        print("数据查询异常")
    db.close()  # 关闭数据库连接
