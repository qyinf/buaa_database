# coding=utf-8
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from food import mysqlPack
import jwt
import hashlib
from random import choice

jwtKey = '123456'
jwtFailedDict = {'code': 666, 'message': 'jwt verified error'}
userField = ['user_id', 'password', 'avatar', 'time', 'real_name', 'sex', 'institute', 'phone',
             'height', 'weight','level']
canteenField = ['canteen_id', 'name', 'floor_count']
foodField = ['food_id', 'name', 'calorie', 'picture', 'place', 'place_id', 'floor', 'price',
             'like', 'dislike', 'intro', 'area', 'isSpicy']
restaurantField = ['restaurant_id', 'name', 'distance']


def hashCode(s, salt='club_system'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def checkJwt(jwtDict: dict) -> bool:
    codeStr: str = jwtDict['code']
    userId = jwtDict['user_id']
    time = jwtDict['time']
    newCodeStr: str = jwt.encode(payload={'user_id': userId, 'time': time}, algorithm='HS256', key=jwtKey,
                                 headers={'typ': 'JWT', 'alg': 'HS256'}).decode()
    return codeStr.__eq__(newCodeStr)


# user
@csrf_exempt # 1130 看过 wjc
def loginUser(request):
    if request.method == 'POST':
        # vars
        userId = request.POST.get('user_id')
        password = request.POST.get('password')
        curTime = str(datetime.now())
        code = jwt.encode(payload={'user_id': userId, 'time': curTime}, algorithm='HS256', key=jwtKey,
                          headers={'typ': 'JWT', 'alg': 'HS256'})
        jwtDict = {'code': code.encode().decode(), 'user_id': userId, 'time': curTime}
        # logics
        result = mysqlPack.getUser(userId)
        if result:
            if result[0][1] != hashCode(password):
                return JsonResponse({'code': 3, 'message': 'wrong password'})
            else:
                # mysqlPack.writeLoginLog(userId)
                return JsonResponse(
                    {'code': 0, 'message': 'login succeess', 'jwt': jwtDict})
        else:
            return JsonResponse({'code': 2, 'message': 'user not found'})
    else:
        return JsonResponse({'code': 1, 'message': 'expect POST, get GET.'})


@csrf_exempt # 1130 k wjc
def registerUser(request):
    if request.method == 'POST':
        # vars
        userId = request.POST.get('user_id')
        name = request.POST.get('name')
        password = request.POST.get('password')
        sex = request.POST.get('sex')
        institute = request.POST.get('institute')
        phone = request.POST.get('phone')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        try:
            mysqlPack.createUser(userId, hashCode(password), name, sex, institute, phone, height, weight)
            return JsonResponse({'code': 0, 'message': 'create user successfully!'})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 4, 'message': 'duplicated user name'})
    else:
        return JsonResponse({'code': 1, 'message': 'expect POST, get GET.'})

@csrf_exempt
def add_canteen(request):
    if request.method == 'POST':
        # vars
        name = request.POST.get('name')
        floor = request.POST.get('floor')
        try:
            mysqlPack.create_canteen(name, floor)
            return JsonResponse({'code': 0, 'message': '添加食堂 successfully!'})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 4, 'message': '添加失败'})
    else:
        return JsonResponse({'code': 1, 'message': 'expect POST, get GET.'})



@csrf_exempt # 1130 k wjc
def updateUserInformation(request):
    if request.method == 'POST':
        userDict = request.POST
        userId = userDict['user_id']
        realName = userDict['real_name']
        sex = userDict['sex']
        institute = userDict['institute']
        phone = userDict['phone']
        height = userDict['height']
        weight = userDict['weight']
        try:
            mysqlPack.updateUserField(userId, realName, sex, institute, phone, height, weight)
            return JsonResponse({'code': 0, 'message': ''})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 14, 'message': 'error'})
    else:
        return JsonResponse({'code': 1, 'message': 'expect POST, get GET.'})


@csrf_exempt # 1130 k wjc
def getUserInformation(request):
    if request.method == 'POST':
        userId = request.POST.get('user_id')
        try:
            userResultDict = dict()
            result = mysqlPack.getUser(userId)
            for num, field in enumerate(userField):
                userResultDict[field] = result[0][num]
                print(result[0][num])
            return JsonResponse({'code': 0, 'message': '', 'user': userResultDict})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 15, 'message': 'error'})
    else:
        return JsonResponse({'code': 1, 'message': 'expect POST, get GET.'})


@csrf_exempt # 1130 看 wjc
def modifyPassword(request):
    if request.method == 'POST':
        jwtDict = {'code': request.POST.get('jwt[code]'), 'user_id': request.POST.get('jwt[user_id]'),
                   'time': request.POST.get('jwt[time]')}
        if not checkJwt(jwtDict):
            return JsonResponse(jwtFailedDict)
        oldPassword = request.POST.get('old_password')
        newPassword = request.POST.get('new_password')
        userId = jwtDict['user_id']
        # check password
        userResult = mysqlPack.getUser(userId)
        if userResult:
            if userResult[0][1] != hashCode(oldPassword):
                return JsonResponse({'code': 3, 'message': 'wrong password'})
        else:
            return JsonResponse({'code': 2, 'message': 'user not found'})
        # change password
        try:
            mysqlPack.updateUserPassword(userId, hashCode(newPassword))
            return JsonResponse({'code': 0, 'message': ''})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 22, 'message': 'error'})
    else:
        return JsonResponse({'code': 1, 'message': 'expect POST, get GET.'})


@csrf_exempt # 1130 k wjc
def updateAvatar(request):
    if request.method == 'POST':
        userId = request.POST.get('user_id')
        avatar = request.POST.get('avatar')
        # end of file template
        try:
            mysqlPack.updateUserAvatar(userId, avatar)
            return JsonResponse({'code': 0, 'message': ''})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 29, 'message': 'error'})
    else:
        return JsonResponse({'code': 1, 'message': 'expect POST, get GET.'})

@csrf_exempt
def get_food_score(request):
    retDict = dict()
    if request.method == 'POST':
        try:
            result = mysqlPack.get_food_score()
            # print("result")
            resultList = []
            for data in result:
                resultItem = dict()
                resultItem['place'] = data[0]
                resultItem['score'] = data[1]
                resultList.append(resultItem)
            retDict['list'] = resultList
            retDict['canteen_num'] = len(resultList)
            print(retDict['canteen_num'])
            retDict['code'] = 0
            retDict['message'] = ''
            return JsonResponse(retDict)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 6, 'message': 'error in find canteen list'})    
    else:
        return JsonResponse({'code': 1, 'message': 'expect POST, get GET.'})   


@csrf_exempt # 1130 k wjc
def findFood(request):
    retDict = dict()
    if request.method == 'POST':
        userId = request.POST.get('user_id')
        try:
            result = mysqlPack.findFood(userId)
            resultList = []
            for data in result:
                resultItem = dict()
                resultItem['food_id'] = data[0]
                resultItem['name'] = data[1]
                resultItem['calorie'] = data[2]
                resultItem['picture'] = data[3]
                resultItem['place'] = data[4]
                resultItem['floor'] = data[5]
                resultItem['price'] = data[6]
                resultItem['like'] = data[7]
                resultItem['dislike'] = data[8]
                resultItem['intro'] = data[9]
                resultItem['isSpicy'] = data[10]
                resultItem['score'] = data[11]
                resultItem['userlike'] = data[12]
                resultItem['show'] = ''
                resultList.append(resultItem)
            retDict['food_list'] = resultList
            retDict['code'] = 0
            retDict['message'] = ''
            return JsonResponse(retDict)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 6, 'message': 'error in finding food'})
    else:
        return JsonResponse({'code': 1, 'message': 'expect POST, get GET.'})

@csrf_exempt # 1130 k wjc
def getTakeaway(request):
    retDict = dict()
    if request.method == 'POST':
        try:
            keyWord = request.POST.get('key_word')
            result = mysqlPack.getTakeaway(keyWord)
            resultList = []
            for data in result:
                resultItem = dict()
                for num, field in enumerate(takeawayField):
                    resultItem[field] = data[num]
                resultList.append(resultItem)
            retDict['takeaway_list'] = resultList
            retDict['code'] = 0
            retDict['message'] = ''
            return JsonResponse(retDict)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 6, 'message': 'error in finding takeaway'})
    else:
        return JsonResponse({'code': 1, 'message': 'expect POST, get GET.'})


# TODO 要写的
@csrf_exempt
def prepareMeal(request):
    retDict = dict()
    if request.method == 'POST':
        calorie = request.POST.get('calorie')
        place = request.POST.get('place')
        taste = request.POST.get('taste')
        budget = request.POST.get('budget')
        floor = request.POST.get('floor')
        try:
            result = mysqlPack.prepareMeal(place, taste, floor)
            # print(result)
            returnList1 = []
            returnList = []
            i = 0
            for data in result:
                resultItem = dict()
                resultItem['name'] = data[0]
                resultItem['calorie'] = data[1]
                resultItem['picture'] = data[2]
                resultItem['price'] = data[3]
                # print(resultItem)
                returnList1.append(resultItem)
            resultItem0 = choice(returnList1)
            while int(resultItem0.get('price')) > int(budget) or int(resultItem0.get('calorie')) > int(calorie):
                resultItem0 = choice(returnList1)
            returnList.append(resultItem0)
            price0 = int(resultItem0.get('price'))
            calorie0 = int(resultItem0.get('calorie'))
            i = returnList1.index(resultItem0) + 1
            flag = 0
            while i <= len(returnList1):
                if i == len(returnList1) and flag == 0:
                    flag = 1
                    i = 0
                if flag == 1 and i == returnList1.index(resultItem0):
                    break
                if int(returnList1[i].get('price')) + price0 < int(budget) and int(returnList1[i].get('calorie')) + calorie0 < int(calorie):
                    returnList.append(returnList1[i])
                    price0 = price0 + int(returnList1[i].get('price'))
                    calorie0 = calorie0 + int(returnList1[i].get('calorie'))
                if len(returnList) == 3:
                    break
                i = i + 1
                if flag == 0 and i == len(returnList1):
                    i = 0
                    flag = 1
            i = 1
            # print(returnList)
            for data in returnList:
                if i == 1:
                    retDict['dish1'] = data['name']
                    retDict['price1'] = "    " + str(data['price']) + "元"
                    retDict['calorie1'] = "    " + str(data['calorie']) + "千卡"
                    i = i + 1
                    continue
                if i == 2:
                    retDict['dish2'] = data['name']
                    retDict['price2'] = "    " + str(data['price']) + "元"
                    retDict['calorie2'] = "    " + str(data['calorie']) + "千卡"
                    i = i + 1
                    continue
                if i == 3:
                    retDict['dish3'] = data['name']
                    retDict['price3'] = "    " + str(data['price']) + "元"
                    retDict['calorie3'] = "    " + str(data['calorie']) + "千卡"
                    i = i + 1
                    continue

            retDict['code'] = 0
            retDict['message'] = ''
            # print(retDict)
            return JsonResponse(retDict)

        except Exception as e:
            print(e)
            return JsonResponse({'code': 6, 'message': 'error in finding food'})
    else:
        return JsonResponse({'code': 1, 'message': 'expect POST, get GET.'})


def find_canteen_list(request):
    retDict = dict()
    if request.method == 'POST':
        try:
            result = mysqlPack.find_canteen_list()
            # print("result")
            resultList = []
            for data in result:
                resultItem = dict()
                resultItem['name'] = data[0]
                resultItem['id'] = data[1]
                resultList.append(resultItem)
            retDict['data'] = resultList
            # print(resultList)
            retDict['code'] = 0
            retDict['message'] = ''
            return JsonResponse(retDict)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 6, 'message': 'error in find canteen list'})    
    else:
        return JsonResponse({'code': 1, 'message': 'expect POST, get GET.'})   

            

@csrf_exempt
def likeDish(request):
    retDict = dict()
    if request.method == 'POST':
        userId = request.POST.get('user_id')
        foodId = request.POST.get('food_id')
        try:
            result = mysqlPack.foodstatus(userId, foodId, 0)
            resultList = []
            for data in result:
                resultItem = dict()
                resultItem['like'] = data[0]
                resultItem['dislike'] = data[1]
                resultList.append(resultItem)
            retDict['data'] = resultList
            retDict['code'] = 0
            retDict['message'] = ''
            #print(resultList)
            return JsonResponse(retDict)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 6, 'message': 'error in 点赞'})
    else:
        return JsonResponse({'code': 1, 'message': 'expect POST, get GET.'})    
    return

@csrf_exempt
def dislikeDish(request):
    retDict = dict()
    if request.method == 'POST':
        userId = request.POST.get('user_id')
        foodId = request.POST.get('food_id')
        try:
            result = mysqlPack.foodstatus(userId, foodId, 1)
            resultList = []
            for data in result:
                resultItem = dict()
                resultItem['like'] = data[0]
                resultItem['dislike'] = data[1]
                resultList.append(resultItem)
            retDict['data'] = resultList
            retDict['code'] = 0
            retDict['message'] = ''
            return JsonResponse(retDict)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 6, 'message': 'error in 点踩'})
    else:
        return JsonResponse({'code': 1, 'message': 'expect POST, get GET.'})
    return


@csrf_exempt
def addDish(request):
    if request.method == 'POST':
        # vars
        image = request.POST.get('image_url')
        name = request.POST.get('name')
        calorie = request.POST.get('calorie')
        floor = request.POST.get('floor')
        place = request.POST.get('place')
        price = request.POST.get('price')
        intro = request.POST.get('intro')
        taste = request.POST.get('taste')
        try:
            mysqlPack.addDish(image, name, calorie, floor, place, price, intro, taste)
            return JsonResponse({'code': 0, 'message': 'create food successfully!'})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 4, 'message': '添加食物失败'})
    else:
        return JsonResponse({'code': 1, 'message': 'expect POST, get GET.'})


@csrf_exempt
def delete_food(request):
    if request.method == 'POST':
        # vars
        print("ssss")
        foodId = request.POST.get('food_id')
        try:
            mysqlPack.delete_Dish(foodId)
            return JsonResponse({'code': 0, 'message': 'delete food successfully!'})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 4, 'message': '删除食物失败'})
    else:
        return JsonResponse({'code': 1, 'message': 'expect POST, get GET.'})