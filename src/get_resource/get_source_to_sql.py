# 将文章中的数据爬取写入数据库
import requests
from bs4 import BeautifulSoup

from src.http_request import mysql_use


def getOnesContent():
    req = requests.get(url='http://wufazhuce.com')
    req.encoding = 'utf-8'
    html = req.text

    chapter_bs = BeautifulSoup(html, 'lxml')
    chapters = chapter_bs.find_all(attrs={'class': 'item active'})
    if len(chapters) == 0:
        return
    chapter = chapters[0]
    image = chapter.find_all(attrs={'class': 'fp-one-imagen'})[0].get('src')
    content = chapter.find_all(attrs={'class': 'fp-one-cita'})[0].text.replace('\n', '')
    number = chapter.find_all(attrs={'class': 'titulo'})[0].text
    date = chapter.find_all(attrs={'class': 'dom'})[0].text + ' ' + chapter.find_all(attrs={'class': 'may'})[0].text

    # 插入数据库
    param = {'image': image,
             'content': content,
             'number': number,
             'date': date
             }
    sql = mysql_use.insertSqlStr('ones', param)
    print('sql = {}'.format(sql))
    cnn = mysql_use.connect_sql()
    res = mysql_use.insert_info(cnn, sql)
    cnn.close()
    return res


if __name__ == '__main__':
    getOnesContent()
