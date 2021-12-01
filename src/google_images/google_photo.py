import base64
import os
import re
import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

here = os.getcwd()


def request_download(image_url, directory, filename):
    path = here + '/' + directory + '/' + filename
    if directory is None or directory == '':
        path = here + '/' + filename

    try:
        if 'data:image' in image_url:
            # base64转图片
            image_url = image_url.split('base64,')[1]
            _img_data = base64.b64decode(image_url)
            with open(path, 'wb') as f:
                f.write(_img_data)
        else:
            # http下载
            r = requests.get(image_url)
            with open(path, 'wb') as f:
                f.write(r.content)

        print('下载成功--> %s' % image_url)
        return True
    except IOError as error:
        print('下载失败--> %s' % image_url)
        print(error)
        return False


# 下载大图url
def down_load_big_img(pic_name):
    time.sleep(1)
    # 获取弹出框
    div_show = driver.find_element(by=By.ID, value='islsp')

    #  找到大图位置，位置可以右键元素 COPY XPATH
    html = div_show.find_element(by=By.XPATH,
                                 value='//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img')
    img_url = html.get_property('src')

    # 获取图片后缀
    suffix = 'png'
    if 'data:image' in img_url:
        # base64文件
        suffix = img_url.split(';')[0].replace('data:image/', '')
    elif '.' in img_url:
        # url中带有后缀
        original_url = img_url
        if '?' in img_url:
            original_url = img_url.split('?')[0]
            suffix = original_url.split('.')[-1]
            if '/' in suffix:
                suffix = 'png'

    elif 'fmt=' in img_url:
        # 带有格式的url
        pattern = re.compile(r'fmt=[a-zA-z0-9]+&')
        compile_result = pattern.findall(img_url)
        if len(compile_result) > 0:
            suffix = compile_result[0].replace('fmt=', '').replace('&', '')

    # 下载后保存名称
    save_name = pic_name + '.' + suffix

    # 创建存储目录
    os.makedirs(key_word, exist_ok=True)
    # 开始下载
    success = request_download(img_url, key_word, save_name)

    # url写入text
    try:
        if success:
            path = here + '/' + key_word + '/urls.text'
            with open(path, 'a') as f:
                f.write(img_url + '\n')
    except IOError:
        print('url write error')
    return img_url


def get_image_url():
    time.sleep(3)
    # 获取根视图
    islrc_box = driver.find_element(by=By.CLASS_NAME, value='islrc')
    div_boxs = islrc_box.find_elements(by=By.XPATH, value='./*')
    normal_class = div_boxs[0].get_attribute('class')
    count = len(div_boxs)
    for index in range(len(images), count):
        div_box = div_boxs[index]
        if normal_class != div_box.get_attribute('class'):
            print('非正常div，跳过: %s', div_box.get_attribute('class'))
            continue
        print('(%d/%d)开始下载' % (index, count))
        try:
            img = div_box.find_element(by=By.TAG_NAME, value='img')
            img.click()
            time.sleep(1)
            img_url = down_load_big_img('%d' % index)
            # img_url = image.get_attribute("src") #缩略图
            images.append(img_url)
            if len(images) > 500:
                driver.__exit__()
                break
        except BaseException as error:
            print(error.__class__)
    # 滚动页面
    if len(images) < total_count:
        time.sleep(2)
        driver.execute_script('return document.body.scrollHeight')
        get_image_url()
    return images


def test():
    image_url = 'https://inews.gtimg.com/newsapp_bt/0/11929928804/1000'
    image_url = 'https://lh3.googleusercontent.com/proxy/YrtE8YhnqS4gym-yrMKzK3Z0AsZ-nuEYOGyx0IMO7blup-mhtg7maNaMg3nC_WdRcrSmqueBfq5JiQmnfhHZjbznFOHH6CM-UOyGc_-Fpb0TtyaJo8LUgKcSRpY1zznpWGkXFemgpsUvaBycsU52xHQ'
    request_download(image_url, '', 'test.png')
    quit()


if __name__ == '__main__':
    # test()

    # 创建一个参数对象，用来控制chrome是否以无界面模式打开
    ch_op = Options()
    # 设置谷歌浏览器的页面无可视化，如果需要可视化请注释这两行代码
    ch_op.add_argument('--headless')
    ch_op.add_argument('--disable-gpu')

    key_word = '鹿晗'
    num = 10
    start = 1
    url = "https://www.google.com/search?&tbm=isch&q=%s&num=%d&start=%d&tbs=isz:l" % (
        key_word, num, start)
    driver = webdriver.Chrome(service=Service('./chromedriver'), options=ch_op)
    driver.get(url)

    total_count = 200
    images = []
    get_image_url()

    key_word = '原神'
    images.clear()
    get_image_url()

    key_word = '英雄联盟壁纸'
    images.clear()
    get_image_url()
    driver.__exit__()
