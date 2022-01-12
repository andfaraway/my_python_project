# coding=utf-8
import socket

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request
from gevent import pywsgi

from src import config
from . import api
from . import api_push
from . import http_result
from .error_code import *
from .http_result import request_has_empty

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
    name = request.args.get('name')
    platform = request.args.get('platform')
    open_id = request.args.get('openId')
    icon = request.args.get('icon')
    if request_has_empty(name, platform, open_id):
        return http_result.dic_format(ErrorCode.CODE_202)

    r_list = api.third_login(name, platform, open_id, icon)
    if r_list is None or len(r_list) == 0:
        return http_result.dic_format(ErrorCode.CODE_201)
    else:
        dic: map = r_list[0]
        dic['userId'] = dic['id']
        del dic['id']
        return http_result.dic_format(data=[dic])


# 注册推送 用户id：user_id, 推送id：push_token, 别名：alias
@app.route("/registerNotification", methods=['post'])
def registerNotification():
    result = api_push.register_notification(**request.args)
    print(result)
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


# 早晨推送
def say_morning(alias, alert):
    scheduler = BackgroundScheduler()

    # 在 2019-8-30 01:00:01 运行一次 job 方法
    scheduler.add_job(api_push.push_alias, 'date', run_date='2021-12-22 18:16:00', args=[alias, alert])

    # 在 2019-08-29 22:15:00至2019-08-29 22:17:00期间，每隔1分30秒 运行一次 job 方法
    scheduler.add_job(api_push.push_alias, 'interval', days=1, start_date='2021-12-22 08:30:00',
                      end_date='2022-01-01 06:00:00', args=[alias, alert])
    scheduler.start()


# 煮蛋提醒
def steam_egg():
    scheduler = BackgroundScheduler()
    # 在 2019-08-29 22:15:00至2019-08-29 22:17:00期间，每隔1分30秒 运行一次 job 方法
    # scheduler.add_job(api_push.push_alias, 'interval', days=1, start_date='2022-01-01 07:19:00',
    #                   end_date='2022-01-01 06:00:00', args=[['Ivy'], '记得蒸蛋哦🥚 ', 'Good Morning！'])
    scheduler.add_job(api_push.push_all, 'interval', days=1, start_date='2022-01-01 07:15:00',
                      end_date='2024-01-01 06:00:00', args=['记得蒸蛋哦🥚 ', 'Good Morning！'])
    scheduler.start()


def happy_morning():
    scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
    scheduler.add_job(api_push.push_alias, 'date', run_date='2022-01-04 09:28:00',
                      args=[['Ivy'], '爱你哟😘', '❤️❤️❤️'])
    scheduler.start()


# 打招呼
@app.route("/sayHello", methods=['get', 'post'])
def say_hello():
    alias = request.args.get('alias').split(',')
    alert = request.args.get('alert')
    if http_result.request_has_empty(alias, alert):
        return http_result.dic_format(ErrorCode.CODE_202)

    api_push.push_alias(alias=alias, alert=alert)
    return http_result.dic_format()


# 检查更新
@app.route("/checkUpdate", methods=['get', 'post'])
def checkUpdate():
    platform = request.args.get('platform')
    version = request.args.get('version')
    if http_result.request_has_empty(platform, version):
        return http_result.dic_format(ErrorCode.CODE_202)
    data = api.checkUpdate(platform)[0]

    update = False
    server_version: list = data['version']
    arr_app = version.split('.')
    arr_server = server_version.split('.')
    for i in range(len(arr_app)):
        if int(arr_app[i]) < int(arr_server[i]):
            update = True
            break
    data['update'] = update
    return http_result.dic_format(data=[data])


def start():
    # 启动接口服务
    if config.isDebug:
        app.run('0.0.0.0', 5000)
    else:
        _server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
        _server.serve_forever()


if __name__ == "__main__":
    start()
