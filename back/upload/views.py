import time

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

from back.settings import MEDIA_ROOT

PIC_URL_BASE = 'http://localhost:8000/'


@csrf_exempt
def uploadImage(request):
    # file template
    file = request.FILES.get('file')
    fileName = file.name
    try:
        # 图片格式
        imageFormat = fileName.split('.')[-1]
        if imageFormat not in ['jpeg', 'jpg', 'png', 'bmp', 'tif', 'gif']:
            return JsonResponse({'code': -2, 'message': '图片格式有误'})
        # 图片路径
        if not os.path.exists(MEDIA_ROOT):
            os.makedirs(MEDIA_ROOT)
        newName = str(time.time()).replace('.', '') + fileName
        imagePath = os.path.join(MEDIA_ROOT, newName)
        print(imagePath)
        # 导入图片
        with open(imagePath, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)
        f.close()
        print(PIC_URL_BASE + imagePath)
        return JsonResponse({'code': 0, 'message': '', 'image_path': PIC_URL_BASE + 'static/' + newName})
    except Exception as e:
        print(e)
        return JsonResponse({'code': -2, 'message': '图片存储错误'})
