import configparser
import os

isDebug = True
# isDebug = False

info = {}


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


def get(key, item='default'):
    if len(info.keys()) == 0:
        init()
    # noinspection PyBroadException
    try:
        return info[item][key]
    except Exception:
        return None
