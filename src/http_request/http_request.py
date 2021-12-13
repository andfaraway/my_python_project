# coding=utf-8
from flask import Flask, request
from gevent import pywsgi

from . import api
from . import http_result

app = Flask(__name__)


@app.route("/login", methods=['get', 'post'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    if username is None or password is None:
        return http_result.dic_format(code=201, msg='Parameters are missing')

    r_list = api.login(username, password)
    print('r_list = {}'.format(r_list))
    result_dic = r_list[1:]

    if result_dic is None or len(result_dic) == 0:
        return http_result.dic_format(code=203, msg='failure')
    else:
        return http_result.dic_format(code=200, msg='success', data=result_dic)


@app.route("/")
def main_func():
    return "Hello World!"


@app.route("/images")
def get_src():
    import os
    path = os.getcwd()
    path = path.replace('my_python_project', 'default/src/')

    files = os.listdir(path)

    files_list = []
    for file in files:
        if os.path.isdir(path + file):
            files_list.append(file)

    dic = {}
    for dir_name in files_list:
        files = os.listdir(path + dir_name + '/')
        dic[dir_name] = files
    return http_result.dic_format(200, '', dic)


# 获取已有图片分类
@app.route("/getPictureCategory")
def getPictureCategory():
    res = api.getPictureCategory()
    return http_result.dic_format(data=res)


# 根据分类获取图片
@app.route("/getPictures", methods=['get', 'post'])
def getPictures():
    category = request.args.get('category')
    res = api.getPicturesWithCategory(category)
    return http_result.dic_format(data=res)


def start():
    app.run()
    # _server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    # _server.serve_forever()


if __name__ == "__main__":
    start()
