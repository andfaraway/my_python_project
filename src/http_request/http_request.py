# coding=utf-8
import datetime
import socket
import time

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request
from gevent import pywsgi
from jpush import JPushFailure
from requests import Response

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


# 登录
@app.route("/login", methods=['post', 'get'])
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


# 获取所有消息
@app.route("/getMessages", methods=['post'])
def getMessages():
    alias = request.args.get('alias')
    r_list = api_push.get_messages(alias)

    # 将date转换成时间戳传给客户端
    try:
        for dic in r_list:
            time1: datetime.datetime = dic['date']
            time_str = str(time1.timestamp()).split('.')[0]
            dic['date'] = time_str
    except BaseException as exception:
        print(exception)
    return http_result.dic_format(data=r_list)


# 删除指定消息
@app.route("/deleteMessage", methods=['post'])
def deleteMessage():
    message_id = request.args.get('id')
    res = api_push.delete_messages(message_id)
    if res == 0:
        return http_result.dic_format()
    else:
        return http_result.dic_format(ErrorCode.CODE_201)


# 插入登录表
@app.route("/insertLaunchInfo", methods=['post'])
def insertLaunchInfo():
    res = api.insert_launch_info(**request.args)
    return http_result.dic_format()


# 插入推送token
@app.route("/pushDeviceToken", methods=['post'])
def pushDeviceToken():
    res = api.pushDeviceToken(**request.args)
    return http_result.dic_format()


# 添加收藏
@app.route("/addFavorite", methods=['post'])
def addFavorite():
    userid = request.args.get('userid')
    content = request.args.get('content')
    source = request.args.get('source')
    if request_has_empty(userid, content):
        return http_result.dic_format(ErrorCode.CODE_202)

    res = api.addFavorite(userid, content, source)
    if res == 1:
        return http_result.dic_format()
    elif type(res) == list:
        return http_result.dic_format(ErrorCode.CODE_201, msg='已收藏')
    else:
        return http_result.dic_format(ErrorCode.CODE_201)


# 查询收藏
@app.route("/getFavorite", methods=['post'])
def getFavorite():
    userid = request.args.get('userid')
    if request_has_empty(userid):
        return http_result.dic_format(ErrorCode.CODE_202)
    r_list = api.getFavorite(userid)
    # 将date转换成时间戳传给客户端
    try:
        for dic in r_list:
            time1: datetime.datetime = dic['date']
            time_str = str(time1.timestamp()).split('.')[0]
            dic['date'] = time_str
    except BaseException as exception:
        print(exception)
    return http_result.dic_format(data=r_list)


# 删除收藏
@app.route("/deleteFavorite", methods=['post'])
def deleteFavorite():
    userid = request.args.get('userid')
    favorite_id = request.args.get('favoriteId')
    if request_has_empty(userid, favorite_id):
        return http_result.dic_format(ErrorCode.CODE_202)
    res = api.deleteFavorite(userid, favorite_id)
    if res == 1:
        return http_result.dic_format()
    else:
        return http_result.dic_format(ErrorCode.CODE_201)


# 添加反馈
@app.route("/addFeedback", methods=['post'])
def addFeedback():
    userid = request.args.get('userid')
    content = request.args.get('content')
    nickname = request.args.get('nickname')
    if request_has_empty(userid, content):
        return http_result.dic_format(ErrorCode.CODE_202)

    res = api.addFeedback(userid, content, nickname)
    if res == 1:
        return http_result.dic_format()
    else:
        return http_result.dic_format(ErrorCode.CODE_201)


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
    if checkToken() is None:
        return http_result.dic_format(ErrorCode.CODE_300)
    picture_id = request.args.get('id')
    res = api.deletePictureWithId(picture_id)
    code = ErrorCode.CODE_200
    if res != 1:
        code = ErrorCode.CODE_201
    return http_result.dic_format(code)


# 版本更新推送
@app.route("/versionUpdate", methods=['post'])
def versionUpdate():
    platform = request.args.get('platform')
    if http_result.request_has_empty(platform):
        return http_result.dic_format(ErrorCode.CODE_202)
    # 从数据库读取最新版本信息
    version_data = api.checkUpdate(platform)[0]

    alias = request.args.get('alias')
    title = version_data.get('title')
    alert = version_data.get('content')
    if http_result.request_has_empty(alert):
        return http_result.dic_format(ErrorCode.CODE_202)
    try:
        if alias is None:
            api_push.push_all(alert=alert, title=title)
        else:
            api_push.push_alias(alias=alias, alert=alert, title=title)
        return http_result.dic_format(data=version_data)
    except JPushFailure as failure:
        return http_result.dic_format(error_code=ErrorCode.CODE_201, msg=failure.error['message'])


# 早晨推送
def say_morning(alias, alert):
    scheduler = BackgroundScheduler()

    # 在 2019-8-30 01:00:01 运行一次 job 方法
    scheduler.add_job(api_push.push_alias, 'date', run_date='2021-12-22 18:16:00', args=[alias, alert])

    # 在 2019-08-29 22:15:00至2019-08-29 22:17:00期间，每隔1分30秒 运行一次 job 方法
    scheduler.add_job(api_push.push_alias, 'interval', days=1, start_date='2021-12-22 08:30:00',
                      end_date='2022-01-01 06:00:00', args=[alias, alert])
    scheduler.start()


def good_morning():
    scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
    scheduler.add_job(say_tuwei, 'interval', days=1, start_date='2022-01-01 06:30:00',
                      end_date='2024-01-01 06:00:00')
    scheduler.start()


def good_afternoon():
    scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
    scheduler.add_job(sayGodReceived, 'interval', days=1, start_date='2022-01-01 12:00:00',
                      end_date='2024-01-01 06:00:00')
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


def say_tuwei():
    tianApi = 'http://api.tianapi.com'
    secretKey = "e1d306002add9c529feaa829d3969766"
    url = '{}/saylove/index?key={}'.format(tianApi, secretKey)
    req: Response = requests.get(url=url, )
    req.encoding = 'utf-8'
    if req.status_code == 200:
        try:
            str_to_dict = eval(req.content)
            content = str_to_dict['newslist'][0]['content']
            api_push.push_all(content, '早安❤')
        except BaseException as error:
            print(error)
            return None
    return None


# 获取神回复
@app.route("/getGodReceived", methods=['get'])
def getGodReceived():
    date2 = '2022/03/02:00:00:00'
    # 获取自定义
    d1 = datetime.datetime.now()
    d2 = datetime.datetime.strptime(date2, '%Y/%m/%d:%H:%M:%S')
    d = d1 - d2

    id = 357 + d.days
    res = api.getGodReceived(id)
    dic = None
    if len(res) > 0:
        dic = res[0]
    return http_result.dic_format(data=dic)


# 发送神回复
def sayGodReceived():
    date2 = '2022/03/02:00:00:00'
    # 获取自定义
    d1 = datetime.datetime.now()
    d2 = datetime.datetime.strptime(date2, '%Y/%m/%d:%H:%M:%S')
    d = d1 - d2

    id = 357 + d.days
    res = api.getGodReceived(id)
    dic = None
    if len(res) > 0:
        dic = res[0]
    print(dic)
    if dic is not None:
        api_push.push_all(alert=dic['question'], save_title=dic['question'], save_content=dic['answer'])
    return http_result.dic_format()


# 获取当天桌面图片
@app.route("/getDesktopImage", methods=['get'])
def getDesktopImage():
    image_id = request.args.get('id')
    if image_id is None:
        # 获取前一天图片
        time_now = datetime.datetime.now()
        image_id = (time_now + datetime.timedelta(days=-1)).strftime("%Y%m%d")
        print(image_id)

    res = api.getDesktopImage(image_id)
    return http_result.dic_format(data=res)


# 获取用户信息
@app.route("/getUserInfo", methods=['get'])
def getUserInfo():
    userid = request.args.get('userid')
    res = api.getUserInfo(userid)
    dic = res
    return http_result.dic_format(data=dic)


# 获取启动页信息
@app.route("/getLaunchInfo", methods=['get'])
def getLaunchInfo():
    date_str = request.args.get('date')
    date = None
    if date_str is not None:
        date = datetime.datetime.strptime(date_str, '%Y%m%d')
    dic = api.getLaunchInfo(date)
    return http_result.dic_format(data=dic)


def start():
    # 启动接口服务
    if config.isDebug:
        app.run('0.0.0.0', 5000)
    else:
        _server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
        _server.serve_forever()


if __name__ == "__main__":
    start()
