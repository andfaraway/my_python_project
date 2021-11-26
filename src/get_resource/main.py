import requests
from bs4 import BeautifulSoup
import utils.file_util
import utils.shell_util
import tqdm

server = 'http://47.241.172.52:9010'


# 获取协作仓库urls
def get_urls():
    headers = {'Cookie': 'lang=zh-CN; i_like_gogs=d67df1653b2b45d9',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
               'Connection': 'keep-alive'}
    req = requests.get(url=server, headers=headers)
    req.encoding = 'utf-8'
    html = req.text
    bs = BeautifulSoup(html, 'lxml')
    chapters = bs.find('ul', id='collaborative-repo-list').find_all('a')

    url_list = []
    for chapter in chapters:
        content_url = server + chapter.get('href')
        url_list.append(content_url)
    return url_list


# 获取具体仓库地址
def get_clone_url(url_str):
    headers = {
        'Cookie': 'lang=zh-CN; confluence.list.pages.cookie=list-content-tree; confluence.browse.space.cookie=space-blogposts; NX-ANTI-CSRF-TOKEN=0.7668772282374894; _ga=GA1.4.1071677221.1627552823; i_like_gogs=c0aae425f0cead30; JSESSIONID=C2DC3E6BABB549665BD426F18AE55BE0; grafana_session=6d502643160a8afaf0cbfb045919383a; _csrf=JE3ZNjWu5-yy7OOn8MZiV5-WcDU6MTYzNzc0NzMxODE4MzM1Mzc3MQ',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
        'Connection': 'keep-alive'}
    req = requests.get(url=url_str, headers=headers)
    req.encoding = 'utf-8'
    html = req.text
    bs = BeautifulSoup(html, 'lxml')
    url1 = bs.find('button', id='repo-clone-https').get('data-link')
    url2 = bs.find('button', id='repo-clone-ssh').get('data-link')
    return {'http': url2, 'ssh': url1}


# 将写入仓库地址写入文件
def write_text():
    # 删除之前的缓存
    utils.shell_util.run_cmd('rm -rf codes\n')
    # 创建文件夹
    utils.shell_util.run_cmd('mkdir codes')

    lists = get_urls()
    for index in range(len(lists)):
        data = get_clone_url(lists[index])
        http_url = data['http']
        ssh_url = data['ssh']
        utils.file_util.add('./codes/http_urls.text', http_url + '\n')
        utils.file_util.add('./codes/ssh_urls.text', ssh_url + '\n')
        print('(%d/%d)please wait...' % (index, len(lists)))
    print('写完了，准备运行clone')


if __name__ == '__main__':
    write_text()
    urls = utils.file_util.read('./codes/ssh_urls.text').split('\n')
    tqdm.tqdm(utils)
    for index in range(len(urls)):
        url = urls[index]
        if url is None or len(url) == 0:
            continue
        ssh_command = 'cd ./codes\ngit clone ' + url
        print('(%d/%d)begin->%s' % (index + 1, len(urls), ssh_command,))
        utils.shell_util.run_cmd(ssh_command)
