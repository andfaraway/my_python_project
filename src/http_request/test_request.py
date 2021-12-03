import os

import mysql_use
from utils.log_util import *


def insert_url_to_photo_show_images(category, name, url):
    sql = 'INSERT INTO photo_show_images(category, name,url) VALUES (\'{}\',\'{}\',\'{}\')'.format(category, name, url)
    cnn = mysql_use.connect_sql()
    res = mysql_use.insert_info(cnn, sql)
    print(res + sql)


def insert_to_photo_show_images_category(category):
    sql = 'INSERT INTO photo_show_images_category(category) VALUES (\'{}\')'.format(category)
    cnn = mysql_use.connect_sql()
    res = mysql_use.insert_info(cnn, sql)
    print(res + sql)


def write_to_sql():
    path = '/Users/libin/Desktop/downloads'
    files = os.listdir(path)
    for category in files:
        file_path = path + '/{}/urls.text'.format(category)
        if os.path.exists(file_path):
            insert_to_photo_show_images_category(category)
            with open(file_path, 'r') as f:
                debug_print('开始读取：{}'.format(file_path))
                text_list = f.read().split('\n')
                for text in text_list:
                    if 'http' in text:
                        name = text.split('):')[0][1:]
                        url = text.split('):')[-1]
                        insert_url_to_photo_show_images(category, name, url)

# write_to_sql()
