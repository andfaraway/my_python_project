from . import mysql_use


# 登录
def login(username, password):
    sql = "select * FROM user where username = \'%s\' and password = \'%s\'" % (username, password)
    print('sql=' + sql)
    cnn = mysql_use.connect_sql()
    res = mysql_use.search_info(cnn, sql)
    return res


# 注册
def register(username, password):
    sql = 'INSERT INTO user(username, password) VALUES (\'{}\',\'{}\')'.format(username, password)
    print('sql=' + sql)
    cnn = mysql_use.connect_sql()
    res = mysql_use.insert_info(cnn, sql)
    return res


# 注销
def delete(username, password):
    sql = 'DELETE FROM user WHERE username = \'{}\''.format(username)
    print('sql=' + sql)
    cnn = mysql_use.connect_sql()
    res = mysql_use.insert_info(cnn, sql)
    return res


# 更新
def update(username, nickname):
    sql = 'UPDATE user SET nick_name = \'{}\' WHERE username = \'{}\''.format(nickname, username)
    print('sql=' + sql)
    cnn = mysql_use.connect_sql()
    res = mysql_use.insert_info(cnn, sql)
    return res
