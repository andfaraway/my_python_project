# coding=utf-8
from flask import Flask, request
from gevent import pywsgi

from . import api
from . import http_result
from .error_code import *

app = Flask(__name__)


# 检查token
def checkToken():
    token = request.args.get('token')
    if token is None:
        return None
    result = api.check_token(token)
    if len(result) == 0:
        return None
    else:
        return result[0]['id']


@app.route("/login", methods=['post'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    if username is None or password is None:
        return http_result.dic_format(ErrorCode.CODE_201)

    r_list = api.login(username, password)
    result_dic = r_list

    if result_dic is None or len(result_dic) == 0:
        return http_result.dic_format(ErrorCode.CODE_201)
    else:
        return http_result.dic_format(data=result_dic)


# 第三方登录
# platform : 1.QQ  2.微信
@app.route("/thirdLogin", methods=['post'])
def third_login():
    name = request.args.get('name')
    platform = request.args.get('platform')
    open_id = request.args.get('openId')
    icon = request.args.get('icon')
    if request_has_empty(name, platform, open_id):
        return http_result.dic_format(ErrorCode.CODE_202)

    r_list = api.third_login(name, platform, open_id, icon)

    result_dic = r_list

    if result_dic is None or len(result_dic) == 0:
        return http_result.dic_format(ErrorCode.CODE_201)
    else:
        return http_result.dic_format(data=result_dic)


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
    return http_result.dic_format(data=dic)


# 获取已有图片分类
@app.route("/getPictureCategory")
def getPictureCategory():
    if checkToken() is None: return http_result.dic_format(ErrorCode.CODE_300)
    res = api.getPictureCategory()
    return http_result.dic_format(data=res)


# 根据分类获取图片
@app.route("/getPictures", methods=['get', 'post'])
def getPictures():
    if checkToken() is None: return http_result.dic_format(ErrorCode.CODE_300)
    category = request.args.get('category')
    res = api.getPicturesWithCategory(category)
    return http_result.dic_format(data=res)


# 删除图片
@app.route("/deletePicture", methods=['get', 'post'])
def deletePicture():
    if checkToken() is None: return http_result.dic_format(ErrorCode.CODE_300)
    picture_id = request.args.get('id')
    res = api.deletePictureWithId(picture_id)
    code = ErrorCode.CODE_200
    if res != 1:
        code = ErrorCode.CODE_201
    return http_result.dic_format(code)


# 判断参数缺失
def request_has_empty(*args):
    for a in args:
        if a is None:
            return True
    return False


def start():
    # app.run()
    _server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    _server.serve_forever()


if __name__ == "__main__":
    start()
