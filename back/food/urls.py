"""back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    # user
    # TODO 
    path('login_user', views.loginUser), # 1130 k 
    path('register_user', views.registerUser), # 1130 k w
    path('update_user_information', views.updateUserInformation), # 1130 k wjc
    path('get_user_information', views.getUserInformation), # 1130 k wjc
    path('modify_password', views.modifyPassword), # 1130 k wjc
    path('update_avatar', views.updateAvatar), # 1130 k wjc
    # club
    # TODO
    path('find_food', views.findFood), # 查找一个食堂的所有食物
    # TODO
    path('get_takeaway',views.getTakeaway),
    # TODO 要自己实现的函数
    path('prepare_meal',views.prepareMeal),
    path('like_dish',views.likeDish),
    path('dislike_dish',views.dislikeDish),
    
    
    # TODO 
    path('add_dish',views.addDish), 

    # TODO 读取食堂列表
    path('find_canteen_list', views.find_canteen_list),

    # TODO 读取食堂点赞数
    path('get_Score', views.get_food_score),

    # TODO 删除食物
    path('delete_food', views.delete_food),

    # TODO 添加食堂
    path('add_canteen', views.add_canteen),
]
