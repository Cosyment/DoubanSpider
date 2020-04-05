DROP TABLE IF EXISTS t_movie;
create table t_movie
(
    id           bigint primary key not null auto_increment,
    title        varchar(100)       not null comment '片名',
    alias        varchar(200) comment '别名',
    language     varchar(100) comment '语言',
    cover        varchar(150) comment '封面图',
    rating       varchar(4) comment '评分',
    year         varchar(5) comment '年份',
    director     varchar(100) comment '导演',
    writer       varchar(50) comment '编剧',
    actors       varchar(100) comment '主演',
    `type`       varchar(50) comment '类型',
    release_date varchar(100) comment '上映日期',
    area         varchar(50) comment '上映地区',
    duration     varchar(20) comment '时长',
    introduction varchar(1000) comment '简介',
    trailer      varchar(100) comment '预告片',
    ranking      int                         default 0 comment '豆瓣排名',
    hot          tinyint(1)                  default 0 comment '是否热门 0-普通，1-热门',
    latest       tinyint(1)                  default 0 comment '是否最新 0-普通，1-最新',
    create_time  TIMESTAMP          NOT NULL DEFAULT CURRENT_TIMESTAMP comment '创建时间',
    update_time  TIMESTAMP          NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间'
) default character set 'utf8mb4' comment '全部电影';

DROP TABLE IF EXISTS t_television;
create table t_television
(
    id           bigint primary key not null auto_increment,
    title        varchar(100)       not null comment '片名',
    alias        varchar(200) comment '别名',
    language     varchar(100) comment '语言',
    cover        varchar(150) comment '封面图',
    rating       varchar(4) comment '评分',
    year         varchar(5) comment '年份',
    director     varchar(100) comment '导演',
    writer       varchar(50) comment '编剧',
    actors       varchar(100) comment '主演',
    `type`       varchar(50) comment '类型',
    count        varchar(20) comment '集数',
    release_date varchar(100) comment '上映日期',
    area         varchar(50) comment '上映地区',
    duration     varchar(50) comment '单集时长',
    introduction varchar(1000) comment '简介',
    trailer      varchar(100) comment '预告片',
    hot          tinyint(1) default 0 comment '是否热门 0-普通，1-热门',
    latest       tinyint(1) default 0 comment '是否最新 0-普通，1-最新',
    create_time  TIMESTAMP          NOT NULL DEFAULT CURRENT_TIMESTAMP comment '创建时间',
    update_time  TIMESTAMP          NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间'
) default character set 'utf8mb4' comment '全部电视';

DROP TABLE IF EXISTS t_animation;
create table t_animation
(
    id           bigint primary key not null auto_increment,
    title        varchar(100)       not null comment '片名',
    alias        varchar(200) comment '别名',
    language     varchar(100) comment '语言',
    cover        varchar(150) comment '封面图',
    rating       varchar(4) comment '评分',
    year         varchar(5) comment '年份',
    director     varchar(100) comment '导演',
    writer       varchar(50) comment '编剧',
    actors       varchar(100) comment '主演',
    `type`       varchar(50) comment '类型',
    count        varchar(20) comment '集数',
    release_date varchar(100) comment '上映日期',
    area         varchar(50) comment '上映地区',
    duration     varchar(50) comment '单集时长',
    introduction varchar(1000) comment '简介',
    trailer      varchar(100) comment '预告片',
    hot          tinyint(1) default 0 comment '是否热门 0-普通，1-热门',
    latest       tinyint(1) default 0 comment '是否最新 0-普通，1-最新',
    create_time  TIMESTAMP          NOT NULL DEFAULT CURRENT_TIMESTAMP comment '创建时间',
    update_time  TIMESTAMP          NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间'
) default character set 'utf8mb4' comment '全部动漫';


DROP TABLE IF EXISTS t_variety;
create table t_variety
(
    id           bigint primary key not null auto_increment,
    title        varchar(100)       not null comment '片名',
    alias        varchar(200) comment '别名',
    language     varchar(100) comment '语言',
    cover        varchar(150) comment '封面图',
    rating       varchar(4) comment '评分',
    year         varchar(5) comment '年份',
    director     varchar(100) comment '导演',
    writer       varchar(50) comment '编剧',
    actors       varchar(100) comment '主演',
    `type`       varchar(50) comment '类型',
    count        varchar(20) comment '集数',
    release_date varchar(100) comment '上映日期',
    area         varchar(50) comment '上映地区',
    duration     varchar(50) comment '单集时长',
    introduction varchar(1000) comment '简介',
    trailer      varchar(100) comment '预告片',
    hot          tinyint(1) default 0 comment '是否热门 0-普通，1-热门',
    latest       tinyint(1) default 0 comment '是否最新 0-普通，1-最新',
    create_time  TIMESTAMP          NOT NULL DEFAULT CURRENT_TIMESTAMP comment '创建时间',
    update_time  TIMESTAMP          NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间'
) default character set 'utf8mb4' comment '全部综艺';

DROP TABLE IF EXISTS `t_movies_area`;
create table `t_movies_area`
(
    `id`    bigint primary key not null auto_increment,
    `title` varchar(100)       not null comment '地区名',
    `type`  varchar(10)        not null default '0' comment '类型 0-电影，1-电视，2-动漫，3-综艺'
) default character set 'utf8mb4' comment '电影地区';

DROP TABLE IF EXISTS `t_movies_channel`;
create table `t_movies_channel`
(
    `id`    bigint primary key not null auto_increment,
    `title` varchar(100)       not null comment '分类名',
    `type`  varchar(10)        not null default '0' comment '类型 0-电影，1-电视，2-动漫，3-综艺'
) default character set 'utf8mb4' comment '电影分类';

DROP TABLE IF EXISTS `t_movies_year`;
create table `t_movies_year`
(
    `id`    bigint primary key not null auto_increment,
    `title` varchar(100)       not null comment '年代',
    `type`  varchar(10)        not null default '0' comment '类型 0-电影，1-电视，2-动漫，3-综艺'
) default character set 'utf8mb4' comment '电影年代';

DROP TABLE IF EXISTS `t_crawl_record`;
create table t_crawl_record
(
    id          bigint primary key not null auto_increment,
    type tinyint(1) not null comment '失败类型 0-电影，1-电视，2-动漫，3-综艺',
    position    int comment '当前页条数',
    page        int comment '当前页数',
    name        varchar(50) comment '电影名',
    create_time TIMESTAMP          NOT NULL DEFAULT CURRENT_TIMESTAMP comment '创建时间',
    update_time TIMESTAMP          NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间'
) comment '记录抓取失败时位置';

