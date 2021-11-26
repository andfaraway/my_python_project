import pymysql
import re


# 打开数据库连接
def connect_sql():
    host = '1.14.252.115'
    user = 'root'
    passwd = 'mysqljmrx'
    db = 'nothing'

    conn = pymysql.connect(host=host, user=user, passwd=passwd, )
    conn.select_db(db)
    return conn


# 查询数据库数据
def search_info(temp_cnn, sql_str):
    sql_str = 'select * from user'
    # 获取游标
    cursor = temp_cnn.cursor()
    # 获取查询结果元组
    cursor.execute(sql_str)
    data_tup = cursor.fetchall()

    # 获取字段名
    fields = cursor.description
    dic = {}
    for index in range(len(fields)):
        key = fields[index][0]
        value = data_tup[0][index]
        dic[key] = value
    cursor.close()
    return dic


# 匹配账号密码
def check(username, password):
    sql = "select * FROM user where username = \'%s\' and password = \'%s\'" % (username, password)
    print('sql=' + sql)
    cnn = connect_sql()
    res = search_info(cnn, sql)
    return res
    cnn.close()

# try:
#     # 执行SQL语句
#     cursor.execute(sql)
#     res = cursor.fetchall()
#     print(res[0][1])
#
#     # 向数据库提交
#     conn.commit()
# except:
#     # 发生错误时回滚
#     print('error' + conn)
#     conn.rollback()
#
# conn.close()


# def searchInfo():

# cur.execute("select login_password from user where login_name='admin'")
# while 1:
#     res = cur.fetchone()
#     if res is None:
#         break
#     print(res[0])
# cur.close()
#
# conn.commit()
# conn.close()
# print('sql执行成功')
