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
    sql = "select * FROM  favorite where userid = \'{}\' and content =  \'{}\'".format(userid,content)
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
    sql = 'DELETE FROM favorite WHERE userid = \'{}\' and id = \'{}\''.format(userid,favorite_id)
    cnn = mysql_use.connect_sql()
    res = mysql_use.delete_info(cnn, sql)
    cnn.close()
    return res
