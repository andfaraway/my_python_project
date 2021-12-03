# 读取数据
import base64

import requests


def read(path):
    with open(path, 'r') as f:
        text = f.read()
        return text


# 写入数据
def write(path, text: str):
    with open(path, 'w') as f:
        result = text
        f.write(result)


# 追加写入
def add(path, text: str):
    with open(path, 'a') as f:
        result = text
        f.write(result)


# 下载图片
def request_download_pic(image_url, save_path):
    try:
        if 'data:image' in image_url:
            # base64转图片
            image_url = image_url.split('base64,')[1]
            _img_data = base64.b64decode(image_url)
            with open(save_path, 'wb') as f:
                f.write(_img_data)
        else:
            # http下载
            r = requests.get(image_url)
            with open(save_path, 'wb') as f:
                f.write(r.content)

        print('下载成功--> %s' % image_url)
        return True
    except IOError as error:
        print('下载失败--> %s' % image_url)
        print(error)
        return False