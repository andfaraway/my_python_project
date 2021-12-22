# coding=utf-8
import time
from datetime import date

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request
from gevent import pywsgi

from . import api, api_push
from . import http_result
from .http_result import request_has_empty
from .error_code import *
from . import push

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


# 第三方登录  platform : 1.QQ  2.微信
@app.route("/thirdLogin", methods=['post'])
def third_login():
    print(request.args)
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


# 注册推送 用户id：user_id, 推送id：push_token, 别名：alias
@app.route("/registerNotification", methods=['post'])
def registerNotification():
    print(request.args)
    user_id = request.args.get('user_id')
    push_token = request.args.get('push_token')
    alias = request.args.get('alias')
    registration_id = request.args.get('registration_id')

    r_list = api.register_notification(user_id, push_token, alias, registration_id)

    result = r_list

    if result == 0:
        return http_result.dic_format(ErrorCode.CODE_201)
    else:
        return http_result.dic_format()


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


# 按别名推送
def push_alias(alert):
    res = api_push.get_alias()
    alias = []
    for dic in res:
        alia = dic['alias']
        alias.append(alia)
    push.alias(alias, alert=alert)


# 早晨推送
def say_hello():
    scheduler = BackgroundScheduler()

    # 在 2019-8-30 01:00:01 运行一次 job 方法
    # scheduler.add_job(push_alias, 'date', run_date='2021-12-22 18:16:00', args=['早啊'])

    # 在 2019-08-29 22:15:00至2019-08-29 22:17:00期间，每隔1分30秒 运行一次 job 方法
    scheduler.add_job(push_alias, 'interval', days=1, start_date='2021-12-22 08:30:00',
                      end_date='2022-01-01 06:00:00', args=['早啊'])
    scheduler.start()


def start():
    say_hello()
    # app.run()

    _server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    _server.serve_forever()


if __name__ == "__main__":
    start()
