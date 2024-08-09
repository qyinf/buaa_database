drop schema if exists `food_system`;
create schema `food_system` default charset = utf8mb4;
use `food_system`;

-- entity
drop table if exists `user`;
create table `user`
(
    `user_id`   varchar(31)  not null, -- 学号
    `password`  varchar(255) not null,
    `avatar`    varchar(255),
    `time`      varchar(31)  not null, -- 注册时间
    `real_name` varchar(31),
    `sex`       varchar(31),
    `institute` varchar(31),
    `phone`     varchar(31),
    `height` int          not null,
    `weight` int          not null,
    `level`     int, -- 用户权限 
    primary key (`user_id`),
    check ( 0 <= `level` and `level` <= 1 ) -- 不同学生 1/管理员 0 权限
);


# canteen
drop table if exists `canteen`;
create table `canteen`
(
    `canteen_id`   int auto_increment not null,
    `name`         varchar(31)        not null,
    `floor_count`  int                not null,
    -- 新增，用于引入触发器，描述食物的总数
    -- `dish_count`   int,
    primary key (`canteen_id`),
    check ( 0 <= `floor_count` and `floor_count` <= 4)
);

-- canteenFood(food)
drop table if exists `food`; -- 学校食堂食物
create table `food`
(
    `food_id`       int auto_increment not null,
    `name`          varchar(31)        not null,
    `calorie`       int                not null,
    `picture`       varchar(255)       not null,
    -- 用于描述食物属于哪个食堂; 
    `place_id`      int                not null,
    `floor`         int                not null,
    `price`         int                not null,
    `like`          int                ,
    `dislike`       int                ,
    `intro`         varchar(255),
    -- 为了防止出现bool类型的坑，1表示辣，2表示不辣
    `isSpicy`       int,
    `score`         int,
    primary key (`food_id`),
    foreign key (`place_id`) references `canteen` (`canteen_id`) on delete cascade,
    check ( 0 <= `floor` and `floor` <= 4)
);

-- restaurant
drop table if exists `restaurant`;
create table `restaurant`
(
    `restaurant_id`       int auto_increment not null,
    `name`          varchar(31)        not null,
    -- 用于描述距离
    `distance`         int                not null,
    `dish_count`       int,
    primary key (`restaurant_id`)
);

-- takeawayFood
drop table if exists `takeaway`;
create table `takeaway`
(
    `takeaway_id`       int auto_increment not null,
    `name`              varchar(31)        not null,
    `calorie`           int                not null,
    `picture`           varchar(255)       not null,
    `place_id`     int                not null,
    `price`             int                not null,
    -- 为了防止出现bool类型的坑，1表示辣，2表示不辣
    `isSpicy`           int,
    `score`             int,
    `like`              int,
    `dislike`           int,
    `intro`             varchar(255),
    primary key (`takeaway_id`),
    foreign key (`place_id`) references `restaurant` (`restaurant_id`) on delete cascade
);

drop table if exists `dish1`; -- 是否喜欢食堂的饭菜
create table `dish1`
(
    `user_id`       varchar(31)        not null,
    `food_id`          int        not null,
    -- 用于描述s是否喜欢 喜欢1 不喜欢 -1 无评价0
    `like`         smallint                ,
    primary key (`user_id`, `food_id`),
    foreign key (`food_id`) references `food` (`food_id`) on delete cascade,
    foreign key (`user_id`) references `user` (`user_id`) on delete cascade
);

drop table if exists `dish2`; -- 是否喜欢某个外卖
create table `dish2`
(
    `user_id`       varchar(31)        not null,
    `takeaway_id`          int        not null,
    -- 用于描述s是否喜欢 喜欢1 不喜欢 -1
    `like`         smallint               ,
    primary key (`user_id`, `takeaway_id`),
    foreign key (`takeaway_id`) references `takeaway` (`takeaway_id`) on delete cascade,
    foreign key (`user_id`) references `user` (`user_id`) on delete cascade
);