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
    print(path)
    try:
        if 'data:image' in image_url:
            # base64转图片
            image_url = image_url.strip()
            image_url = image_url + '==='
            print('%d:%s' % (len(image_url), image_url))
            _img_data = base64.b64decode(image_url)
            with open(path, 'wb') as f:
                f.write(_img_data)
        else:
            # http下载
            r = requests.get(image_url)
            with open(path, 'wb') as f:
                f.write(r.content)

        print('下载成功--> %s' % image_url)
    except IOError as error:
        print('下载失败--> %s' % image_url)


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
    suffix = 'jpg'
    if 'data:image' in img_url:
        # base64文件
        suffix = img_url.split(';')[0].replace('data:image/', '')
    elif '.' in img_url:
        # url中带有后缀
        original_url = img_url
        if '?' in img_url:
            original_url = img_url.split('?')[0]
        suffix = original_url.split('.')[-1]
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
    request_download(img_url, key_word, save_name)
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
    bs = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAR4AAACwCAMAAADudvHOAAAA/FBMVEX/////8+YAAAD+9eb0re/0ru3/8+f/9' \
         '+j/++v/+Ov/9OTn5+ft7e3/++3//OwAAALz8/P5' \
         '+fna2trOzs6amppTU1PHx8d5eXlCQkKPj48oKCixsbEWFhY9PT3h4eGkpKQgICBhYWHU1NS8vLxxcXGCgoIuLi5JSUlpaWnNx7' \
         '+dnZ22trbz6+AzMzMNDQ1ON0+rgKe4jbReRF4vJDOHaYyWdJl7Ynv9uPuwfquzea39r/mMaITJl8dBMD' \
         '/fo97lq99wUm0bCx0jFiFoR2fQocwsISj1tvBbRFdsU3HGvLWXkYnc08SnoppYU0qPjYRZWVm6tKm2rKQsJx95cmgglVlRAAAIfUlEQVR4nO2d+1caSRbH6aq2X1rtIyKKgKDyyjTMZjZZdtzJYyZZdgCjEv///2XurYKmCoVxf7E41P3knMRGc06d76m672oLBYIgCIIgCIIgCIIgCIIgCIIgCIIgCOK1ObS9gA3mvNhnrbczhU5Kp7322ZHdFW0QRy0mKV/iQ1s9sGvaT5I3LOe8cLx4qNpe2Eawh1L8/I93v0hJ8K9/vv/wr334t2l7aZtAA4T4MPD9wb8Z24c/7NfhzY0//Bk+3rW9Nvvsggz/GewAg99Qn4+ffMlnEOrM9uLscw7yfPZBHf/G/8TYL8MbJc/gC2OnthdnnzOQRG4e1OTTr76/o+Tx4awxcl4lxr7k8ujAUWN7tldnnSZjX0melVww9vvAX5IHHm/ocCGXoMJvy7sHHocQBxVtL24DaM1ssymPPFvntte2AcDpYu9udgz8neFH+Nj20jaCCmN/DE15dgYfaPPMOAElvhr6+P43iJ8pJVVcy7zCX8hzM/wvfFSzva5NoQxivB9ohud/8MGF7VVtDDUsY3wZ+kN5xPzBn/DYsL2oDeII9fn4WR0wTEbJ8Bjs1rHS826wMxwOce/UKV42OCziBno/vAF19ln9wPZ6No4zecC+4ckqUyr6lJN5Db5F6jzHgerh9MjurADbOFRBXU2tU5p/dfKGGhWFw4Nnj9I5BtLs9Oq1l7NZnDQqrNJ4s/zxYWNupa9trGpDyFUomq7qoLXoJJdW/N/t56CuN9c1qljNmETeCH/g0tbybINuvDXtTltLpwjLh4045DzO+ox17C3QKtge7cRRGIVjUx94aIuEA9GtuxVV2DSnoYeIbl2zMrh5JiHHb8QTZ3tdOHrQVfJ4cfaD5QMHVThaKZfyeJmzRUPIsPazRMnDw6w+rw/WwC53YyUPnzg7xYIJ6FwezwtxnzCMAiFxr/OZag7bHiygTnJ5kgg3CjsqFHpghaKZPOl3dz0XqDEOc3mSaIT67NU0k8Qzh5tdJcbKsbdA4EmqwtnqB8HsxE3hE1frhjiQOtL1Se9meUSkzlwgIHC8t71Ma5Tl9uG5PInoYD0ezlayOFvu5uxXaH0E1/ZPfIq7J+ZKHhlNu3q2gKKMjzV5Ahn+PAglT9xyOWFXgXMvSJLFBlLuvRthVBh24csnpSCXOAdbUxI8j34gCUVNVMqVgmtr2V6hXbAeNhKaPDx6wB5pFnIe9Bk7tr1AuxziXsl068xTNMjVIAlHzuZbCzD4qerBD+cpjvvcC/Dy1NORreNHocvD4yKYpGbcpxGfgvLuD1Ggb6Cgh/vH2UqYwUEfXZV+vhKsMWP43La9tk0AzU/PMwgnT9sXzvIWC/FGcuGp8Idu20rQzNwuoh9EVjccDwpzKloNbK5PE8wP3amQ1J5Eh6APxD102VbxE5pnUx8eYHXjre2VbQZncJQascc1hYIMz9yJ7ZVtBpicQvKubyDl3t3sAj4BL/jfpsb5SjF7pxuBhcLRcRMTUTaKdHkScO/7lJceneZzPkZ2Ae6r5PQElCSfZ8Zx+ExPTr0g/M4cT9zldZN657rdR33apncPecXlCbHCzCZHIhYeNkWN4g84eum+KrbXaI8r6bGSIEg8keG9nLFZHEtRNFfnEORNyep82olLfR5SPTtNxDV85myztMfYeC6PmpZjXcN9BVnZ4W5pGS1PHi3LQk8/M/SR/UBX579bhjyeHAirBoHuwGT046j3ajN2p8nDRVP2cXTzE+CohnvB897l1VWtJE3zwlcF4h5M8V2qyxNN3RtleVPMo+VuqMfKQQ/0uTWyLwEGvGd7wa+K9oJCVuW6PCHeFTDdVzxyrPRzvhBnH8+SZmsS1acwioc46+PQxf8DFGCaBUH2gEdpKdQRWOi5fTKX6U7scyynnBIgijtyrxj6gHuvTPQDl6Dz+sn2ql+NXp57Jol4xPtbMV949yCIsoAbja+06FBouGc0tuIG6NMxC81LBNHYoboqNrYWFyq4h0WNcbpOHqcmDaU8i7aounAyFt7KDRQ4dYFgzwxsVNELh5zXbKCeQ6+YhTx9vIiLOVeVjHXnC3INJ2zz0cXx+d41Yy0jbVATzbfxKnVkz337i4Y19RoRLLA/GCOXSp9gpTyxC579Ssu0mN604VxMcEZ+te1pbf+Ys3xrfv2+wuTs4Hdz4jLMplm4QpsgmTiQlJalfRFeVx2xR72qA1FzuNqxQ2i99WEhHi3ZhwhjebWfNYUXaPLwlfLIO8nbbpnBX32fdSVkBYexu3SNtdFIOw6Um6sY7Sh5IOksq1DnJfrIsGjrX2VY1cruSRg0VKic/J1AgSeqDhhmHAF71LoSsbxb+xgl67Tx5qX47S8WvmXshyZPIqZP/NezyDGN7b9ggWHPZNGVSBIhq8qjVdHO/Kce3SgVHsIuuBO6qZGpxJpMC9VJpxBEbn0+gTSXOxCQanWa4TrbnEivVbe98ldhV5qaRLfFPI7XmuYkRq/lyO2TpupQrNNjCWl4tj0XnXPYZ6yS8ZfrE6Nzc+fqCY6hyhenvUwdabr77vT/CiVwQ4/pC+VRNdZtz7UM2jITfZE88aTiRsSjIV92OY5ecL6EVMcVszxnV1Uy/k6eQA1quHfjraYyrbWpBOydqZvqzPRpZ+Fq/56Eobyi49rJUshfS1GZiOf1CSCXV78I2LF5whz11vyHFaWMMLyVzTBHUonnKEkDHRvJuqrGJ+FEXvBqOBQNPgXfrMuKmViWJ5zIcTG3b3EV1EtlsdizyFCTJIy7j1KcU9ffbFQo7KlLkuOJEFEUCSGyUWnWX3Zlkmc9Z0qMemM8vh2XqvPm+/GWt0NfTC3/lQs5vQsSZ8FRydDm2GFnvoLLi9J9q1ztnF1tf7OGIAiCIAiCIAiCIAiCIAiCIAiCIAiCIAiCIP5P/gLGAKgUV6MNpQAAAABJRU5ErkJggg== '
    request_download(bs,  '', 'test.png')
    quit()


if __name__ == '__main__':
    test()

    # 创建一个参数对象，用来控制chrome是否以无界面模式打开
    ch_op = Options()
    # 设置谷歌浏览器的页面无可视化，如果需要可视化请注释这两行代码
    # ch_op.add_argument('--headless')
    # ch_op.add_argument('--disable-gpu')

    key_word = '比心'
    num = 10
    start = 1
    url = "https://www.google.com/search?&tbm=isch&q=%s&num=%d&start=%d&tbs=isz:l" % (
        key_word, num, start)
    driver = webdriver.Chrome(service=Service('./chromedriver'), options=ch_op)
    driver.get(url)

    total_count = 100
    images = []

    image_urls = get_image_url()
    driver.__exit__()
