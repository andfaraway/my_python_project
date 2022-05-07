import datetime

from lunar_python import Lunar, Solar
from pymysql import NULL

from . import mysql_use


# 验证token
def check_token(token):
    sql = "select id FROM user where token = \'%s\'" % token
    print('sql=' + sql)
    cnn = mysql_use.connect_sql()
    res = mysql_use.search_info(cnn, sql)
    cnn.close()
    return res


# 登录
def login(username, password):
    sql = "select * FROM user where username = \'%s\' and password = \'%s\'" % (username, password)
    print('sql=' + sql)
    cnn = mysql_use.connect_sql()
    res = mysql_use.search_info(cnn, sql)
    cnn.close()
    return res


# 注册
def register(username, password):
    sql = 'INSERT INTO user(username, password) VALUES (\'{}\',\'{}\')'.format(username, password)
    print('sql=' + sql)
    cnn = mysql_use.connect_sql()
    res = mysql_use.insert_info(cnn, sql)
    cnn.close()
    return res


# 第三方登录  platform : 1.QQ  2.微信
def third_login(name, platform=1, open_id=None, avatar=None):
    cnn = mysql_use.connect_sql()

    # 1.查询绑定关系
    sql = "select * FROM user_binding where open_id = \'{}\' ".format(open_id)
    res = mysql_use.search_info(cnn, sql)

    if len(res) == 0:
        # 绑定表中没有，创建新账户
        sql = 'INSERT INTO user(username,nick_name, password, avatar) VALUES (\'{}\',\'{}\',\'{}\',\'{}\')'.format(name,
                                                                                                                   name,
                                                                                                                   '123456',
                                                                                                                   avatar)
        mysql_use.insert_info(cnn, sql)

        sql = "select * FROM user where username = \'{}\' ".format(name)
        res = mysql_use.search_info(cnn, sql)
        print('res={}'.format(res))
        # 新账户关联绑定表
        user_id = res[0]['id']
        sql = 'INSERT INTO user_binding(user_id, open_id, platfrom) VALUES (\'{}\',\'{}\',\'{}\')'.format(user_id,
                                                                                                          open_id,
                                                                                                          platform)
        mysql_use.insert_info(cnn, sql)
        return res

    else:
        user_id = res[0]['user_id']
        sql = "select * FROM user where id = \'{}\' ".format(user_id)
        res = mysql_use.search_info(cnn, sql)
        return res


# 注销
def delete(username, password):
    sql = 'DELETE FROM user WHERE username = \'{}\''.format(username)
    print('sql=' + sql)
    cnn = mysql_use.connect_sql()
    res = mysql_use.delete_info(cnn, sql)
    cnn.close()
    return res


# 更新
def update(username, nickname):
    sql = 'UPDATE user SET nick_name = \'{}\' WHERE username = \'{}\''.format(nickname, username)
    print('sql=' + sql)
    cnn = mysql_use.connect_sql()
    res = mysql_use.insert_info(cnn, sql)
    cnn.close()
    return res


# 获取图片分类
def getPictureCategory():
    sql = "select * FROM  photo_show_images_category"
    print('sql=' + sql)
    cnn = mysql_use.connect_sql()
    res = mysql_use.search_info(cnn, sql)
    cnn.close()
    return res


# 根据分类获取图片
def getPicturesWithCategory(category):
    sql = "select * FROM  photo_show_images where category = \'{}\'".format(category)
    print('sql=' + sql)
    cnn = mysql_use.connect_sql()
    res = mysql_use.search_info(cnn, sql)
    # 只取id
    result = []
    for dic in res:
        temp_dic = {'id': dic['id'], 'category': category, 'url': dic['url']}
        result.append(temp_dic)
    cnn.close()
    return result


# 删除图片
def deletePictureWithId(picture_id):
    sql = 'DELETE FROM photo_show_images WHERE id = \'{}\''.format(picture_id)
    print('sql=' + sql)
    cnn = mysql_use.connect_sql()
    res = mysql_use.delete_info(cnn, sql)
    cnn.close()
    return res


# 检查更新 根据平台获取最新版本
def checkUpdate(platform):
    sql = "select * FROM  version_update where platform = \'{}\' order by version DESC".format(platform)
    cnn = mysql_use.connect_sql()
    res = mysql_use.search_info(cnn, sql)
    cnn.close()
    return res


# 获取收藏
def getFavorite(userid):
    sql = "select * FROM  favorite where userid = \'{}\' order by date DESC".format(userid)
    cnn = mysql_use.connect_sql()
    res = mysql_use.search_info(cnn, sql)
    cnn.close()
    return res


# 添加收藏
def addFavorite(userid, content, source):
    # 查询是否已收藏
    sql = "select * FROM  favorite where userid = \'{}\' and content =  \'{}\'".format(userid, content)
    cnn = mysql_use.connect_sql()
    res = mysql_use.search_info(cnn, sql)
    if len(res) != 0:
        return res

    sql = "INSERT INTO favorite(userid, content, source) VALUES (\'{}\',\'{}\',\'{}\')".format(userid, content, source)
    print('sql=' + sql)
    res = mysql_use.insert_info(cnn, sql)
    cnn.close()
    return res


# 删除收藏
def deleteFavorite(userid, favorite_id):
    sql = 'DELETE FROM favorite WHERE userid = \'{}\' and id = \'{}\''.format(userid, favorite_id)
    cnn = mysql_use.connect_sql()
    res = mysql_use.delete_info(cnn, sql)
    cnn.close()
    return res


# 添加反馈
def addFeedback(userid, content, nickname=None):
    sql = "INSERT INTO feedback(userid, content, nickname) VALUES (\'{}\',\'{}\',\'{}\')".format(userid, content,
                                                                                                 nickname)
    cnn = mysql_use.connect_sql()
    res = mysql_use.insert_info(cnn, sql)
    cnn.close()
    return res


# 添加桌面图片
def addDesktopImage(image_id, name, image_format, url):
    param = {'id': image_id,
             'name': name,
             'format': image_format,
             'url': url
             }
    sql = mysql_use.insertSqlStr('desktop_image', param)
    print('sql = {}'.format(sql))
    cnn = mysql_use.connect_sql()
    res = mysql_use.insert_info(cnn, sql)
    cnn.close()
    return res


# 获取桌面图片
def getDesktopImage(image_id):
    sql = "select * FROM  desktop_image where id = \'{}\'".format(image_id)
    cnn = mysql_use.connect_sql()
    res = mysql_use.search_info(cnn, sql)
    cnn.close()
    return res


# 获取神回复
def getGodReceived(id=0):
    sql = "select * FROM funny where id = \'{}\'".format(id)
    cnn = mysql_use.connect_sql()
    res = mysql_use.search_info(cnn, sql)
    cnn.close()
    return res


# 插入登录表
def insert_launch(**kwargs):
    param = {'userid': kwargs.get('userid'),
             'username': kwargs.get('username'),
             'version': kwargs.get('version'),
             'alias': kwargs.get('alias'),
             'registrationID': kwargs.get('registrationID'),
             'battery': kwargs.get('battery'),
             'device_info': kwargs.get('device_info'),
             'network': kwargs.get('network'),
             }
    sql = mysql_use.insertSqlStr('launch', param)
    cnn = mysql_use.connect_sql()
    res = mysql_use.insert_info(cnn, sql)
    cnn.close()
    return res


# 插入推送token
def pushDeviceToken(**kwargs):
    param = {'userid': kwargs.get('userid'),
             'deviceToken': kwargs.get('deviceToken'),
             'debug': kwargs.get('debug')
             }
    sql = mysql_use.insertSqlStr('push_token', param)
    print(sql)
    cnn = mysql_use.connect_sql()
    res = mysql_use.insert_info(cnn, sql)
    cnn.close()
    return res


# 获取登录信息
def getUserInfo(userid):
    sql = "select * FROM launch where userid = \'{}\' order by date DESC".format(userid)
    if userid is None:
        sql = "select * FROM launch"
    cnn = mysql_use.connect_sql()
    res = mysql_use.search_info(cnn, sql)
    cnn.close()
    return res


# 获取获取设置模块
def getSettingModule(account_type):
    sql = "select * FROM config where account_type = \'{}\' or account_type = '0'".format(account_type)
    cnn = mysql_use.connect_sql()
    res = mysql_use.search_info(cnn, sql)
    cnn.close()
    return res


# 获取英文月份
def getEnMonth(month):
    switch = {1: 'January',
              2: 'February',
              3: 'March',
              4: 'April',
              5: 'May',
              6: 'June',
              7: 'July',
              8: 'August',
              9: 'September',
              10: 'October',
              11: 'November',
              12: 'December',
              }
    return switch[month]


# 获取启动页信息
def getLaunchInfo(date):
    if date is None:
        date = datetime.datetime.now()

    # 农历
    lunar = Lunar.fromDate(date)
    # 阳历
    solar = Solar.fromDate(date)

    # 获取节日
    festival = ''
    if len(solar.getFestivals()) > 0:
        festival = solar.getFestivals()[0]
    elif len(lunar.getFestivals()) > 0:
        festival = lunar.getFestivals()[0]
    else:
        festival = lunar.getJieQi()

    # 内容
    sql = "select * from launch_info order by id DESC limit 1"
    print('sql=' + sql)
    cnn = mysql_use.connect_sql()
    res = mysql_use.search_info(cnn, sql)
    cnn.close()
    dic = res[0]

    if dic['festival'] is not None:
        festival = dic['festival']
    contentStr = dic['content']
    image = dic['image']
    authorStr = dic['author']
    qr_code = dic['qr_code']
    backgroundImage = dic['image_background']
    homePage = dic['home_page']
    # 获取内容
    res = {'title': festival,
           'dayStr': '{}'.format(solar.getDay()),
           'monthStr': getEnMonth(solar.getMonth()),
           'dateDetailStr': '星期{} 农历{}月{} 晴'.format(solar.getWeekInChinese(), lunar.getMonthInChinese(),
                                                    lunar.getDayInChinese()),
           'contentStr': contentStr,
           'authorStr': authorStr,
           'codeStr': qr_code,
           'image': image,
           'backgroundImage': backgroundImage,
           'homePage': homePage}
    print(res)
    return res


# 插入启动页信息
def insertLaunchInfo(**kwargs):
    param = {'id': kwargs.get('id'),
             'festival': kwargs.get('festival'),
             'content': kwargs.get('content'),
             'author': kwargs.get('author'),
             'qr_code': kwargs.get('qr_code'),
             'home_page': kwargs.get('home_page'),
             'image': kwargs.get('image'),
             'image_background': kwargs.get('image_background'),
             }
    sql = mysql_use.insertSqlStr('launch_info', param)
    cnn = mysql_use.connect_sql()
    res = mysql_use.insert_info(cnn, sql)
    cnn.close()
    return res


# 插入摸鱼信息
def insertMoyu(content):
    param = {'content': content}
    sql = mysql_use.insertSqlStr('moyu', param)
    cnn = mysql_use.connect_sql()
    res = mysql_use.insert_info(cnn, sql)
    cnn.close()
    return res
