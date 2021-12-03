import requests
import os
from bs4 import BeautifulSoup
from utils import file_util


def main():
    server = 'https://dribbble.com'
    req = requests.get(url=server)
    req.encoding = 'utf-8'
    html = req.text
    file_util.write('./dribbble.html', html)
    chapter_bs = BeautifulSoup(html, 'lxml')
    chapters = chapter_bs.find_all('img')
    for index, chapter in enumerate(chapters):
        url = chapter.get('src')
        if url is not None:
            url = url.split('?')[0]
            s = url.split('.')[-1]
            path = '/Users/libin/Desktop/downloads/追波/{}.{}'.format(index, s);
            file_util.request_download_pic(url,path)


if __name__ == '__main__':
    main()
