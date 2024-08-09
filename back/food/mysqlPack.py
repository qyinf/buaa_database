# coding=utf-8
import pymysql
import os
from back.settings import DATABASES

clubTypeToNum = {'科技': 0, '人文': 1, '实践': 2, '体育': 3, '艺术': 4, '其它': 5}
numToClubType = ['科技', '人文', '实践', '体育', '艺术', '其它']


def connectDatabase():
    database = DATABASES['default']
    connect = pymysql.connect(host=database['HOST'], db=database['NAME'], user=database['USER'],
                              passwd=database['PASSWORD'], charset="utf8")  # replace my password with 123456
    cursor = connect.cursor()
    return connect, cursor


def closeDatabase(connect, cursor):
    connect.close()
    cursor.close()


def initDatabase():
    database = DATABASES['default']
    base = 'back/database/'
    sqlFiles = ['create.sql', 'procedure.sql', 'trigger.sql']
    # excute
    # TODO 如何查看name
    os.system('mysql -V')
    for name in sqlFiles:
        os.system('mysql -u root -p' + database['PASSWORD'] + ' < ' + base + name)



# user 1130 k wjc
def createUser(userId: str, password: str, name: str, sex: str, institute: str, phone: str, height: int, weight: int):
    connect, cursor = connectDatabase()
    try:
        cursor.callproc('createUser', args=(userId, password, name, sex, institute, phone, height, weight))
        connect.commit()
    except Exception as e:
        print(e)
        connect.rollback()
        raise e
    finally:
        closeDatabase(connect, cursor)
    return

def create_canteen(name: str, floor: int):
    connect, cursor = connectDatabase()
    try:
        cursor.callproc('createCanteen', args=(name, floor))
        connect.commit()
    except Exception as e:
        print(e)
        connect.rollback()
        raise e
    finally:
        closeDatabase(connect, cursor)
    return    


# 1130 kan wjc
def getUser(userId: str):
    # 需要userId和用户Id完全匹配
    connect, cursor = connectDatabase()
    try:
        ins = 'select * from user where user_id = %s;'
        cursor.execute(ins, [userId])
        result = cursor.fetchall()
    except Exception as e:
        connect.rollback()
        raise e
    finally:
        closeDatabase(connect, cursor)
    return result

# 1130 g wjc
def updateUserField(userId: str, realName: str, userSex: str, userInstitute: str,
                    userPhone: str, userHeight: int, userWeight: int):
    connect, cursor = connectDatabase()
    try:
        cursor.callproc('updateUserField',
                        (userId, realName, userSex, userInstitute, userPhone, userHeight, userWeight))
        connect.commit()
    except Exception as e:
        print(e)
        connect.rollback()
        raise e
    finally:
        closeDatabase(connect, cursor)

# 1130 k wjc
def updateUserPassword(userId: str, userPassword: str):
    connect, cursor = connectDatabase()
    try:
        cursor.callproc('updatePassword', (userId, userPassword))
        connect.commit()
    except Exception as e:
        print(e)
        connect.rollback()
        raise e
    finally:
        closeDatabase(connect, cursor)

# 1130 k wjc
def updateUserAvatar(userId: str, userAvatar: str):
    connect, cursor = connectDatabase()
    try:
        cursor.callproc('updateAvatar', (userId, userAvatar))
        connect.commit()
    except Exception as e:
        print(e)
        connect.rollback()
        raise e
    finally:
        closeDatabase(connect, cursor)

# 1130 k wjc ，1206修改, 每个用户都要显示的不一样
def findFood(user_id: str):
    connect, cursor = connectDatabase()
    try:
        ins = 'select food.food_id, food.name, calorie, picture, canteen.name, floor, price, food.like, food.dislike, intro, isSpicy, score, dish1.like from food JOIN dish1 Join canteen WHERE user_id = %s AND dish1.food_id = food.food_id and place_id = canteen_id;'
        cursor.execute(ins, [user_id]) 
        result = cursor.fetchall()
    except Exception as e:
        print(e)
        connect.rollback()
        raise e
    finally:
        closeDatabase(connect, cursor)
    #print(result)    
    return result


def foodstatus(user_id: str, food_id: int, op: int):
    connect, cursor = connectDatabase()
    try:
        print(food_id)
        if op == 0:
            cursor.callproc('like_food', (user_id, food_id))
        else:
            cursor.callproc('dislike_food', (user_id, food_id)) 
        connect.commit()    
        ins = 'select `like`, dislike from food where food_id = %s;'
        cursor.execute(ins, [food_id]) 
        result = cursor.fetchall()    
    except Exception as e:
        print(e)
        connect.rollback()
        raise e
    finally:
        closeDatabase(connect, cursor)
    print(result)   
    return result    

# 1130 k wjc
def getTakeaway(keyWord: str):
    connect, cursor = connectDatabase()
    try:
        ins = 'select * from food1 where place_name like %s'
        cursor.execute(ins, ['%' + keyWord + '%'])  # 子串匹配
        result = cursor.fetchall()
    except Exception as e:
        print(e)
        connect.rollback()
        raise e
    finally:
        closeDatabase(connect, cursor)
    return result


def prepareMeal(place: str, taste: int, floor: int):
    connect, cursor = connectDatabase()
    try:
        #print(place, taste)
        ins = 'SELECT name, calorie, picture, price FROM food WHERE place_id = (select canteen_id FROM canteen WHERE name like %s) and isSpicy = %s and floor = %s'
        cursor.execute(ins, [place, taste, floor])
        result = cursor.fetchall()
        print(result)
        connect.commit()
        #print(result)
    except Exception as e:
        print(e)
        # print("except")
        connect.rollback()
        raise e
    finally:
        closeDatabase(connect, cursor)
    return result

# 1206 查找所有的食堂
def find_canteen_list():
    connect, cursor = connectDatabase()
    try:
        ins = 'SELECT name, canteen_id FROM canteen'
        cursor.execute(ins, [])
        result = cursor.fetchall()
        connect.commit()
    except Exception as e:
        print(e)
        connect.rollback()
        raise e
    finally:
        closeDatabase(connect, cursor)
    return result

# 最后绘制图表需要的评分数据
def get_food_score():   
    connect, cursor = connectDatabase()
    try:
        ins = 'SELECT canteen.`name`, SUM(food.`like`) FROM food join canteen on canteen.canteen_id = place_id GROUP BY place_id'
        cursor.execute(ins, [])
        result = cursor.fetchall()
        connect.commit()
    except Exception as e:
        print(e)
        connect.rollback()
        raise e
    finally:
        closeDatabase(connect, cursor)
    return result


def addDish(image: str, name: str, calorie: int, floor: int, place: str, price: int, intro: str, taste: int):
    connect, cursor = connectDatabase()
    try:
        cursor.callproc('addDish', args=(image, name, calorie, floor, place, price, intro, taste))
        connect.commit()
    except Exception as e:
        print(e)
        connect.rollback()
        raise e
    finally:
        closeDatabase(connect, cursor)
    return

def delete_Dish(food_id: int):
    connect, cursor = connectDatabase()
    try:
        cursor.callproc('delete_Dish',
                        (food_id))
        connect.commit()
    except Exception as e:
        print(e)
        connect.rollback()
        raise e
    finally:
        closeDatabase(connect, cursor)