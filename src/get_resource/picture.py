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

HEADER_STRING = '''
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,en;q=0.8
cache-control: max-age=0
cookie: CGIC=IocBdGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2UvYXZpZixpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45; HSID=AKcURlEGzYeYgvZub; SSID=AGVHoJijMVt95D_kt; APISID=e-JLHazKHhsTCV1R/Al9cD0z5t21FrVaXX; SAPISID=s-jwCGUORM6K3I2q/AjRsga53nAdag_wz7; __Secure-1PAPISID=s-jwCGUORM6K3I2q/AjRsga53nAdag_wz7; __Secure-3PAPISID=s-jwCGUORM6K3I2q/AjRsga53nAdag_wz7; OGPC=19025836-2:19026531-1:; SEARCH_SAMESITE=CgQI_ZMB; OTZ=6259803_24_24__24_; SID=EQiSMWmjDZmuf8ITIX6hwmJeKEDFIJrdvrNRbX56E8XmHoIoBrHzjD9shHbXWYbamm2HlQ.; __Secure-1PSID=EQiSMWmjDZmuf8ITIX6hwmJeKEDFIJrdvrNRbX56E8XmHoIoZCO1nwMyWfU0cdDboqt6SQ.; __Secure-3PSID=EQiSMWmjDZmuf8ITIX6hwmJeKEDFIJrdvrNRbX56E8XmHoIoXo_F3FhR0d6nO_Mmixhsdg.; NID=511=Sr9vHPktUtsq9ghZmV34IndFPC02DRxLSGIX1JuMIMniGQU0Lyt2GV4oD_NkamVMgJKtB_xcL1S6R0k3_aoG8pwkPE-B3Hr62xERgI25l7GsWScJuDeDSXL-lJZGzuRWUcXstpF-4b2sVbTt1m5BM09I2Ei7yjlklCHWu3G_LoQiMU4Lg8Ow0kWVZPmFIsbbjcxvkfR8YJDYOJnTNHF8DtJFbjsvPVNyCSrDzTZgth7tcIhU-R2sbEF-aA_0HvXaNVYZye6o8TIkiy_g2AeKHNdni3BX88oqxMARsBcWEeFkOCnpCG1hyi1GmyOj2BgwP0TxMoJYgHuMZmZkTi327gIGhfj0Qj5tKehH0EMuwo0MJEZZfcfShQ7X2Qqa45lc-4YNturS_oZe; DV=w2i2fmI0vSxPEL5WPJip-J-mAeeU1lfFnRULTMb8vQEAAOAeYAAQspMRdQAAAASIm0L1K13fTQAAAA; 1P_JAR=2021-11-29-1; SIDCC=AJi4QfGu6Q5iZGgqV_C_9XYMQOQKGIwFwT5fmO8SZy4U1nz7ERQZrkR1IcRmUL3R32hTYA439qs; __Secure-3PSIDCC=AJi4QfFZu7Ab4r0IH8GFpGOXySZYEF6zs3OX6qMugPU1uFJ2Bb6GzuvQSNKcRkJgdd1DWt7qrw
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "macOS"
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: same-origin
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36
'''


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


def get_google_src(html_url):
    _req = requests.get(url=html_url)
    _req.encoding = 'utf-8'
    _req.headers = get_headers(HEADER_STRING)

    _html = _req.text
    utils.file_util.write('google.html', _html)

    _bf = BeautifulSoup(_html, 'lxml')
    div1 = _bf.find_all('div', attrs={'class': 'jB2rPd'})

    # print(div1)
    # li_list = _bf.find_all('img')
    # list1 = []
    # for chapter in results:
    #     img_src = chapter.get('src')
    #     list1.append(img_src)
    # return list1


def get_headers(headers_str: str):
    headers = {}
    header_list = headers_str.strip().split('\n')
    for string in header_list:
        list = string.split(':')
        key = list[0]
        if len(list) == 2 and key != 'Decoded' and key != 'x-client-data':
            headers[list[0]] = list[1]
    return headers


keyword = 'water'
size = 30
start = 2
url = 'https://www.google.com/search?&tbm=isch&q=%s&num=%d&start=%d&tbs=isz:l' % (keyword, size, start)
url = 'https://www.google.com/search?q=water&newwindow=1&sxsrf=AOaemvJzOBfvX-O6Uq9vWkNMhEmUdnUiCQ:1638149286553&source=lnms&tbm=isch&sa=X&ved=2ahUKEwi4lcHStbz0AhXBfd4KHdQZDOgQ_AUoAXoECAIQAw&biw=1577&bih=896&dpr=1#imgrc=fNyqVGsZx5h7CM'

print(url)
get_google_src(url)

# images = get_images(url, )
# utils.file_util.write('image/images.text', '\n'.join(images))
# images = file_util.read('image/images.text').split('\n')
# utils.shell_util.create(keyword)

# for index, url in enumerate(images):
#     if 'http' not in url: continue
#     print('(%d/%d)开始下载...' % (index + 1, len(images)))
#     print(url)
#     request_download(url, keyword, '%s_%s.jpg' % (keyword, time.time()))
# urllib_download(url, 'google_image')
