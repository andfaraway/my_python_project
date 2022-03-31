import base64
import json
import sys
import time

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Response
from urllib import request

import ssl

print(sys.path[0])
from src.http_request import api

ssl._create_default_https_context = ssl._create_unverified_context


def geturl():
    _url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"
    req: Response = requests.get(url=_url)
    req.encoding = 'utf-8'
    image = None
    if req.status_code == 200:
        map1 = json.loads(req.content)
        image = 'https://www.bing.com' + map1['images'][0]['url']
    return image


# 字节bytes转化K\M\G
def format_size(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except Exception as error:
        print("传入的字节格式不对:{}".format(error))
        return "Error"
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.3fG" % G
        else:
            return "%.3fM" % M
    else:
        return "%.3fKB" % kb


'''
 urllib.urlretrieve 的回调函数：
def callbackfunc(blocknum, blocksize, totalsize):
    @blocknum:  已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
'''


def download_callback(blocknum, blocksize, totalsize):
    global start_time
    speed = (blocknum * blocksize) / (time.time() - start_time)
    speed_str = " Speed: %s/s" % format_size(speed)
    percent = blocknum * blocksize / totalsize

    percent_str = "%.2f%%" % (percent * 100)
    if percent >= 1:
        percent_str = "100%, size:{}".format(format_size(totalsize))

    print('\rdownloading:{},{},'.format(percent_str, speed_str), end='', )


global start_time


def download():
    url = geturl()

    # 获取图片后缀
    suffix = 'jpg'
    image_lower = url.lower()
    if 'jpeg' in image_lower:
        suffix = 'jpeg'
    elif 'png' in image_lower:
        suffix = 'png'
    elif 'gif' in image_lower:
        suffix = 'gif'

    image_id = time.strftime("%Y%m%d", time.localtime())
    name = '{}.{}'.format(image_id, suffix)

    global start_time
    start_time = time.time()
    request.urlretrieve(url, '/data/www/default/src/deskTopImage/' + name, download_callback)

    # 上传数据库
    api.addDesktopImage(image_id, name, 'http://1.14.252.115' + '/src/deskTopImage/' + name)


def start():
    scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
    scheduler.add_job(download, 'interval', days=1, start_date='2022-03-01 00:00:05',
                      end_date='2024-01-01 00:00:00', args=[])
    scheduler.start()

# if __name__ == '__main__':
#     download()
