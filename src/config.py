import configparser
import os
import socket

isDebug = True

info = {}


# 查询本机ip地址
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def init():
    file = os.getcwd() + '/config.ini'
    # 创建配置文件对象
    con = configparser.ConfigParser()
    # 读取文件
    con.read(file, encoding='utf-8')
    # 获取特定section 返回结果为元组
    items = con.items()
    read_info = dict(items)
    for key in read_info.keys():
        value = dict(read_info[key])
        global info
        info[key] = value
    ip = get_host_ip()
    global isDebug
    if ip == '1.14.252.115' or ip == '10.0.20.14':
        isDebug = False

    print('isDebug:{}'.format(isDebug))


def get(key, item='default'):
    if len(info.keys()) == 0:
        init()
    # noinspection PyBroadException
    try:
        return info[item][key]
    except Exception:
        return None
