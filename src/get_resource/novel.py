import requests
from bs4 import BeautifulSoup
from utils import file_util


def get_content(_target):
    _req = requests.get(url=_target)
    _req.encoding = 'utf-8'
    _html = _req.text
    _bf = BeautifulSoup(_html, 'lxml')
    _texts = _bf.find('div', id='content')
    _content = _texts.text.strip().split('\xa0' * 4)
    return _content


# 诡秘之主 /15_15338/
# 临渊行 /91_91546/
if __name__ == '__main__':
    server = 'https://www.biqupai.com'
    book_name = '临渊行.txt'
    target = server + '/91_91546/'
    req = requests.get(url=target)
    req.encoding = 'utf-8'
    html = req.text
    chapter_bs = BeautifulSoup(html, 'lxml')
    chapters = chapter_bs.find('div', id='list')
    chapters = chapters.find_all('a')

    titles = ''
    try:
        titles = file_util.read('title_' + book_name)
    except IOError:
        file_util.write('title_' + book_name, '')

    count = len(chapters)
    for index in range(count):
        chapter = chapters[index]
        chapter_name = chapter.string
        print('(%d/%d)下载中：%s' % (index + 1, count, chapter_name))
        if chapter_name not in titles:
            url = server + chapter.get('href')
            try:
                content = get_content(url)
                file_util.add('title_' + book_name, chapter_name + '\n')
                file_util.add(book_name, text=chapter_name + '\n' + '\n'.join(content) + '\n\n')
            except IOError:
                print(IOError)
                continue
