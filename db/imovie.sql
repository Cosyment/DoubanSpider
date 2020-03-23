create table t_movie
(
    id           bigint primary key not null auto_increment,
    title        varchar(100)       not null comment '片名',
    alias        varchar(100) comment '别名',
    language     varchar(10) comment '语言',
    cover        varchar(100) comment '封面图',
    rating       varchar(4) comment '评分',
    year         varchar(5) comment '年份',
    director     varchar(50) comment '导演',
    writer       varchar(50) comment '编剧',
    actors       varchar(100) comment '主演',
    `type`       varchar(50) comment '类型',
    release_date varchar(100) comment '上映日期',
    area         varchar(20) comment '地区',
    duration     varchar(20) comment '时长',
    introduction varchar(1000) comment '简介',
    trailer      varchar(100) comment '预告片',
    ranking      int comment '豆瓣排名',
    hot          int comment '是否热门 0-普通，1-热门',
    latest       int comment '是否最新 0-普通，1-最新',
    create_time  TIMESTAMP          NOT NULL DEFAULT CURRENT_TIMESTAMP comment '创建时间',
    update_time  TIMESTAMP          NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间'
) default character set 'utf8mb4' comment '全部电影';

create table t_crawl_record
(
    id          bigint primary key not null auto_increment,
    position    int comment '当前页条数',
    page        int comment '当前页数',
    name        varchar(50) comment '电影名',
    create_time TIMESTAMP          NOT NULL DEFAULT CURRENT_TIMESTAMP comment '创建时间',
    update_time TIMESTAMP          NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间'
) comment '记录抓取失败时位置';

