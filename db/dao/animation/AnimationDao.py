from db import DBHelper
import EnumUtil


def insert(insert_type,
           title,  # 电视剧名称
           alias,  # 别名
           language,  # 语言
           cover,  # 封面图
           rating,  # 评分
           year,  # 年代
           director,  # 导演
           writer,  # 编剧
           actors,  # 主演
           type,  # 类型
           release_date,  # 上映日期
           area,  # 地区
           count,  # 集数
           duration,  # 单集时间
           introduction,  # 简介
           trailer_url,  # 预告片
           ):
    db = DBHelper.Connector().get_connection()
    cursor = db.cursor()
    title = title.replace("\'", "\\'")
    alias = alias.replace("\'", "\\'")
    director = director.replace("\'", "\\'")
    actors = actors.replace("\'", "\\'")
    introduction = introduction.replace("\"", "\\\"").replace("\'", "\\'")
    sql = "insert into t_animation(title,alias,language, cover,rating,year, director, writer, actors, type, release_date,area,count, duration, introduction, trailer,latest,hot) " \
          "values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
        title.strip(),
        alias.strip(),
        language.strip(),
        cover.strip(),
        rating,
        year,
        director.strip(),
        writer.strip(),
        actors.strip(),
        type.strip(),
        release_date.strip(),
        area.strip(),
        count.strip(),
        duration.strip(),
        introduction.strip(),
        trailer_url.strip(),
        1 if insert_type == EnumUtil.InsertType.LATEST else 0,
        1 if insert_type == EnumUtil.InsertType.HOT else 0)
    query_sql = "select title from t_animation where title=\'{}'".format(title)
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
                    # update_sql = "UPDATE t_animation t SET  t.latest = 1 WHERE t.title =\'{}'".format(title)
                    update_sql = "UPDATE t_animation t SET t.alia\'{}', t.area=\'{}',t.language=\'{}',t.director=\'{}',t.writer=\'{}', t.actors=\'{}', t.latest = 1 WHERE t.title =\'{}'".format(
                        alias, area, language, director, writer, actors, title)
                    print("----------->>>>更新最新动漫剧信息 《{}》".format(title))
                elif insert_type == EnumUtil.InsertType.HOT:
                    # update_sql = "UPDATE t_animation t SET t.hot = 1 WHERE t.title =\'{}'".format(title)
                    update_sql = "UPDATE t_animation t SET t.alias=\'{}', t.area=\'{}',t.language=\'{}',t.director=\'{}',t.writer=\'{}', t.actors=\'{}',t.hot = 1 WHERE t.title =\'{}'".format(
                        alias, area, language, director, writer, actors, title)
                    print("----------->>>>更新热门动漫剧信息 《{}》".format(title))
                if update_sql is not None:
                    cursor.execute(update_sql)
                    db.commit()
    except Exception as ex:
        print(ex)
        # 如果发生错误则回滚
        db.rollback()
    # 关闭数据库连接
    db.close()
