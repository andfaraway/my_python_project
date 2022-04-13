import datetime
import os

import ajax as ajax
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def insert_img(request):
    """
              @api {POST} /upload/ [上传图片]
               * @apiVersion 0.0.1
               * @apiGroup note
              @apiParamExample {params} 请求参数
                  "image":""       "图片文件"

              """
    image = request.FILES.get("image")
    if not image:
        return ajax.jsonp_fail(request, u"缺少参数")
    service_name = save_block_file(image)
    path = '%s/%s' % ("你的服务器地址", service_name)
    if not path:
        return ajax.jsonp_fail(request, u"上传失败")
    else:
        return ajax.jsonp_ok(request, path)


def save_upload_file(new_file_path, raw_file, name):
    """
    功能说明：保存上传文件
    raw_file:原始文件对象
    new_file_path:新文件绝对路径
    """
    try:
        # 如果新文件存在则删除
        if os.path.exists(new_file_path):
            try:
                os.remove(new_file_path)
            except:
                pass

        content = raw_file.read()
        fp = open(new_file_path, 'wb')
        fp.write(content)
        fp.close()
        return name
    except Exception as e:
        print(e)
        return False


def save_block_file(block_file):
    """
    :param block_file: 文件对象
    :return:
    """
    # 唯一标识 + 文件名   201801171.png
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    name = '%s%s' % (now_time, block_file.name)
    block_file_path = get_absolute_file_path(name).replace("\\", "/")
    # 文件上传保存
    return save_upload_file(block_file_path, block_file, name)


def get_absolute_file_path(file_name):
    """
    功能说明：返回绝对路径字符串
    file_name:文件名字

    """
    media_root = settings.UPLOAD
    print("media_root", media_root)
    absolute_file_path = os.path.join(media_root, file_name)
    print("absolute_file_path", absolute_file_path)
    # 返回文件绝对路径中目录路径
    file_dir = os.path.dirname(absolute_file_path)
    print("file_dir", file_dir)
    if not os.path.exists(file_dir):
        # 创建路径
        os.makedirs(file_dir)
    return absolute_file_path
