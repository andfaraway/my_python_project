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


# 第三方登录
# platform : 1.QQ  2.微信
def third_login(name, platform, open_id, icon=None):
    # 查询是否绑定账号
    sql = "select * FROM user_binding where open_id = \'{}\' ".format(open_id)
    cnn = mysql_use.connect_sql()
    res = mysql_use.search_info(cnn, sql)
    if len(res) == 0:
        register_sql = 'INSERT INTO user_binding(name, platfrom, open_id, icon) VALUES (\'{}\',\'{}\',\'{}\',\'{}\')'.format(
            name, platform, open_id, icon)
        if icon is None:
            register_sql = 'INSERT INTO user_binding(name, platfrom, open_id) VALUES (\'{}\',\'{}\',\'{}\')'.format(
                name, platform, open_id)
        cnn = mysql_use.connect_sql()
        res = mysql_use.insert_info(cnn, register_sql)
        if res == 1:
            res = mysql_use.search_info(cnn, sql)
        else:
            res = []
    cnn.close()
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
