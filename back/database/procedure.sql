# createUser
use food_system;

delimiter ;;
# createUser -- 已修改 1130 wjc 
create
    definer = root@localhost procedure createUser(in userId varchar(31), in UserPassword varchar(255),
                                                  in realName varchar(31), in userSex varchar(31),
                                                  in userInstitute varchar(31), in user_phone varchar(31),
                                                  in user_height int, in user_weight int)
begin
    insert into user(user_id, password, time, real_name, sex, institute, phone, height, weight, level) value
        (userId, UserPassword, from_unixtime(unix_timestamp()), realName, userSex, userInstitute, 0, user_height, user_weight, 0);
    -- 1205,增加有关dish1内容
    INSERT into 
    dish1 (`user_id`, `food_id`) 
    (SELECT user_id, food_id FROM user JOIN food WHERE user_id = userId); 
    update dish1 SET `like` = 0 where  user_id = userId;
    # end
end;;
delimiter ;

delimiter ;;
# createCanteen -- 已修改 1130 wjc 
create
    definer = root@localhost procedure createCanteen(in Name varchar(31), in Floor int)
begin
    insert into canteen(name, floor_count) value
        (Name, Floor);
    # end
end;;
delimiter ;


-- 更新用户信息 1130 wjc
delimiter ;;
# updateUserField
create procedure updateUserField(in userId varchar(31), in realName varchar(31), in userSex varchar(31),
                                 in userInstitute varchar(31), in userPhone varchar(31),
                                 in user_height int, in user_weight int)
begin
    update user
    set real_name = realName,
        sex       = userSex,
        institute = userInstitute,
        phone     = userPhone,
        height    = user_height, 
        weight    = user_weight
    where user_id = userId;
    # end
end;;
delimiter ;

-- 删除食物
delimiter ;;
# delete_Dish
create procedure delete_Dish(in foodId int)
begin
    delete from food where food_id = foodId;
    # end
end;;
delimiter ;


-- 修改用户密码 1130 k wjc
delimiter ;;
# updatePassword
create procedure updatePassword(in userId varchar(31), in userPassword varchar(255))
begin
    update user set password = userPassword where user_id = userId;
    # end
end;;
delimiter ;

-- 修改/上传头像 1130 k wjc
delimiter ;;
# updateAvatar
create procedure updateAvatar(in userId varchar(31), in userAvatar varchar(255))
begin
    update user set avatar = userAvatar where user_id = userId;
    # end
end;;
delimiter ;

-- 增加食堂的食物 1206 w
delimiter ;;
# addDish
create procedure addDish(in f_image varchar(255),
                         in foodName varchar(31), in f_calorie int, 
                         in f_floor int, in f_place varchar(31),
                         in f_price int, in f_intro varchar(255),
                         in f_taste int)
begin
-- 新增食物
    INSERT INTO food 
    (name, calorie, picture, place_id, floor, price, `like`, `dislike`, intro, isSpicy, score) 
    VALUES 
    (foodName, f_calorie, f_image, 
     (select canteen_id FROM canteen where `name` = f_place),
     f_floor, f_price, 0, 0, f_intro, f_taste, 0);
-- 更新dish1表     
    INSERT into 
    dish1 (`user_id`, `food_id`) 
    (SELECT user_id, food_id FROM user JOIN food WHERE food_id = (select food_id from food where food_id = (select max(food_id) from food))); 
    update dish1 SET `like` = 0 where  food_id = (select food_id from food where food_id = (select max(food_id) from food));
    # end
end;;
delimiter ;

-- 点赞
delimiter ;;
# like_food
create procedure like_food(in userId varchar(31), in foodId int)
begin
    update dish1 set `like` = 1 where user_id = userId and food_id = foodId;
    # end
end;;
delimiter ;

delimiter ;;
# dislike_food
create procedure dislike_food(in userId varchar(31), in foodId int)
begin
    update dish1 set `like` = -1 where user_id = userId and food_id = foodId;
    # end
end;;
delimiter ;