from db import DBHelper
import EnumUtil


def insert(insert_type, ranking, title, alias, language, cover, rating, year, director, writer, actors, type,
           release_date, area, duration,
           introduction,
           trailer_url):
    db = DBHelper.Connector().get_connection()
    cursor = db.cursor()
    title = title.replace("\'", "\\'")
    alias = alias.replace("\'", "\\'")
    director = director.replace("\'", "\\'")
    actors = actors.replace("\'", "\\'")
    introduction = introduction.replace("\"", "\\\"").replace("\'", "\\'")

    sql = "insert into t_movie(title,alias,language, cover,rating,year, director, writer, actors, type, release_date, area,duration, introduction, trailer,ranking,latest,hot) " \
          "values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
        title.strip(),
        alias.strip(),
        language.strip(),
        cover.strip(),
        rating,
        year.strip(),
        director.strip(),
        writer.strip(),
        actors.strip(),
        type.strip(),
        release_date.strip(),
        area.strip(),
        duration.strip(),
        introduction.strip(),
        trailer_url.strip(),
        ranking,
        1 if insert_type == EnumUtil.InsertType.LATEST else 0,
        1 if insert_type == EnumUtil.InsertType.HOT else 0
    )
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
            if insert_type == EnumUtil.InsertType.ALL:
                print("----------->>>>已存在该记录 《{}》".format(title))
            else:
                update_sql = None
                if insert_type == EnumUtil.InsertType.LATEST:
                    # update_sql = "UPDATE t_movie t SET t.latest = 1 WHERE t.title =\'{}'".format(title)
                    update_sql = "UPDATE t_movie t SET t.alias=\'{}', t.area=\'{}',t.language=\'{}',t.director=\'{}',t.writer=\'{}', t.actors=\'{}', t.latest = 1 WHERE t.title =\'{}'".format(
                        alias, area, language, director, writer, actors, title)
                    print("----------->>>>更新最新电影信息 《{}》".format(title))
                elif insert_type == EnumUtil.InsertType.HOT:
                    # update_sql = "UPDATE t_movie t SET t.hot = 1 WHERE t.title =\'{}'".format(title)
                    update_sql = "UPDATE t_movie t SET t.alias=\'{}', t.area=\'{}',t.language=\'{}',t.director=\'{}',t.writer=\'{}', t.actors=\'{}', t.hot = 1 WHERE t.title =\'{}'".format(
                        alias, area, language, director, writer, actors, title)
                    print("----------->>>>更新热门电影信息 《{}》".format(title))
                elif insert_type == EnumUtil.InsertType.BEST:
                    # update_sql = "UPDATE t_movie t SET  t.ranking = \'{}' WHERE t.title =\'{}'".format(ranking, title)
                    update_sql = "UPDATE t_movie t SET t.alias=\'{}', t.area=\'{}',t.language=\'{}',t.director=\'{}',t.writer=\'{}', t.actors=\'{}', t.ranking = \'{}' WHERE t.title =\'{}'".format(
                        alias, area, language, director, writer, actors,
                        ranking, title)
                    print("----------->>>>更新最佳电影信息 《{}》".format(title))

                if update_sql is not None:
                    cursor.execute(update_sql)
                    db.commit()
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
