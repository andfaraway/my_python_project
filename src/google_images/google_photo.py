import base64
import os
import re
import time

import requests
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


# 下载图片
def request_download(image_url, save_path):
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


# 下载大图url
def down_load_big_img(pic_name):
    time.sleep(1)
    # 获取弹出框
    div_show = driver.find_element(by=By.ID, value='islsp')

    #  找到大图位置，位置可以右键元素 COPY XPATH
    try:
        html = div_show.find_element(by=By.XPATH,
                                     value='//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img')
        img_url = html.get_property('src')
    except Exception as error:
        print('element no found')
        return 'error element'

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
        else:
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

    # 开始下载
    success = request_download(img_url, download_path + '/' + save_name)
    # url写入text
    try:
        if success:
            text = '({}):{}'.format(save_name, img_url)
            if 'data:image' in img_url: text = '({}):image;base64'.format(save_name)
            path = download_path + '/urls.text'
            with open(path, 'a') as f:
                f.write(text + '\n')
    except IOError:
        print('url write error')
    return img_url


# 获取url
def get_image_url():
    time.sleep(3)
    # 获取根视图
    islrc_box = driver.find_element(by=By.CLASS_NAME, value='islrc')
    print('islrc = {}'.format(islrc_box))
    div_boxs = islrc_box.find_elements(by=By.XPATH, value='./*')
    normal_class = div_boxs[0].get_attribute('class')
    count = len(div_boxs)
    # 从第几张图开始下载
    begin_index = get_begin_index(download_path)
    print('begin_index = {},count={}'.format(begin_index, count))
    if begin_index >= count:
        scroll_to_bottom()
        get_image_url()
        return images
    print('begin_index = {},count={}'.format(begin_index, count))
    for index in range(begin_index, count):
        div_box = div_boxs[index]
        if normal_class != div_box.get_attribute('class'):
            print('非正常div，跳过: %s', div_box.get_attribute('class'))
            continue
        print('%s%s(%d/%d)开始下载' % (current_time(), key_word, index, count))
        print(div_box.find_elements())
        return
        img = div_box.find_element(by=By.TAG_NAME, value='img')
        try:
            img.click()
        except Exception as error:
            print('img不能点击')
            continue
        time.sleep(1)
        img_url = down_load_big_img('%d' % index)
        # img_url = image.get_attribute("src") #缩略图
        images.append(img_url)
        if len(images) > total_count:
            return images

    # 滚动页面
    if len(images) < total_count:
        scroll_to_bottom()
        get_image_url()
    return images


def current_time():
    return time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())


# 获取最后下载图片的index
def get_begin_index(path):
    count = 0
    if os.path.exists(path):
        try:
            with open(path + '/urls.text', 'r') as f:
                list1 = f.read().split('\n')
                count_text = list1[-2].split('.')[0].replace('(', '')
                count = int(count_text) + 1
        except Exception as error:
            count = 0
            print(error)
    return count


# 滚动到页面底部
def scroll_to_bottom():
    js = 'window.scrollTo(0,document.body.scrollHeight)'
    driver.execute_script(js)
    time.sleep(3)


if __name__ == '__main__':
    # 存储路径
    download_root_path = '/Users/libin/Desktop/downloads/'
    download_path = download_root_path

    # 创建一个参数对象，用来控制chrome是否以无界面模式打开
    ch_op = Options()
    # 设置谷歌浏览器的页面无可视化，如果需要可视化请注释这两行代码
    ch_op.add_argument('--headless')
    ch_op.add_argument('--disable-gpu')

    num = 10
    start = 1
    total_count = 200
    images = []

    downloads_list = ['鹿晗手机壁纸']

    print('{}:{}'.format(current_time(), downloads_list))
    while len(downloads_list):
        key_word = downloads_list[0]

        download_path = download_root_path + key_word
        if not os.path.exists(download_path):
            os.mkdir(download_path)
        url = "https://www.google.com/search?&tbm=isch&q=%s&num=%d&start=%d" % (
            key_word, num, start)
        driver = webdriver.Chrome(service=Service('./chromedriver'), options=ch_op)
        driver.get(url)
        images.clear()
        get_image_url()
        print('{}下载完成。'.format(key_word))
        downloads_list.pop(0)
    print(current_time() + '下载完成')
