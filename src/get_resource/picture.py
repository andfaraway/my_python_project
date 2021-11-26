# 创建文件夹
import os
import pathlib
import re
import time
import urllib

import requests
from bs4 import BeautifulSoup

import utils.file_util
from utils import shell_util, file_util, path_util

here = os.getcwd()


def urllib_download(image_url, directory):
    from urllib.request import urlretrieve
    _name = image_url.split('/')[-1]
    path = here + '/' + directory + '/'
    try:
        urlretrieve(image_url, filename=path + _name)
    except IOError:
        utils.shell_util.create(directory)
        urlretrieve(image_url, filename=path + _name)


def request_download(image_url, directory, _filename):
    import requests
    _name = image_url.split('/')[-1]
    path = here + '/' + directory + '/' + _filename
    r = requests.get(image_url)
    with open(path, 'wb') as f:
        f.write(r.content)


def chunk_download(image_url):
    import requests
    r = requests.get(image_url, stream=True)
    with open('./image/img3.png', 'wb') as f:
        for chunk in r.iter_content(chunk_size=32):
            f.write(chunk)


def get_images(_server):
    _req = requests.get(url=_server)
    _req.encoding = 'utf-8'
    _req.headers = {
        # 'Upgrade-Insecure-Requests': '1',
        'sec-ch-ua-platform': "macOS",
        # 'Host': 'image.baidu.com',
        # 'Connection': 'keep - alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
    }
    _html = _req.text
    _bf = BeautifulSoup(_html, 'lxml')
    li_list = _bf.find_all('img')
    list1 = []
    for chapter in li_list:
            img_src = chapter.get('src')
            list1.append(img_src)
    return list1


keyword = u'美女'

url = 'https://www.google.com/search?site=&tbm=isch&source=hp&w=1080&h=1990&q=%s' % keyword
print(url)
images = get_images(url, )
# utils.file_util.write('image/images.text', '\n'.join(images))
# images = file_util.read('image/images.text').split('\n')
utils.shell_util.create(keyword)
for index, url in enumerate(images):
    if 'http' not in url : continue
    print('(%d/%d)开始下载...' % (index + 1, len(images)))
    print(url)
    request_download(url, keyword, '%s_%d_%s.jpg' % (keyword, index, time.time()))
    # urllib_download(url, 'google_image')
