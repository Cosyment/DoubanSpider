create table movie
(
    movie_id     bigint primary key not null auto_increment,
    name         varchar(100)       not null comment '片名',
    cover        varchar(100) comment '封面图',
    rating       varchar(4) comment '评分',
    year         varchar(5) comment '年份',
    director     varchar(50) comment '导演',
    writer       varchar(50) comment '编剧',
    actors       varchar(100) comment '主演',
    `type`       varchar(50) comment '类型',
    release_date varchar(50) comment '上映日期',
    duration     varchar(10) comment '时长',
    introduction varchar(1000) comment '简介',
    trailer      varchar(100) comment '预告片'
)
