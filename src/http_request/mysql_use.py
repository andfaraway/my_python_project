import os

import pymysql
import configparser

file = os.getcwd() + '/config.ini'
# 创建配置文件对象
con = configparser.ConfigParser()
# 读取文件
con.read(file, encoding='utf-8')

# 获取特定section 返回结果为元组
items = con.items('mysql')
# 可以通过dict方法转换为字典
dic = dict(items)

# 读取配置
host = dic.get('host')
user = dic.get('user')
passwd = dic.get('passwd')
db = dic.get('db')


# 打开数据库连接
def connect_sql():
    conn = pymysql.connect(host=host, user=user, passwd=passwd, )
    conn.select_db(db)
    return conn


# 查询数据库数据
def search_info(db, sql_str):
    # 获取游标
    cursor = db.cursor()
    result_list = []
    try:
        # 获取查询结果元组
        cursor.execute(sql_str)
        data_tup = cursor.fetchall()
        fields = cursor.description
        if not len(data_tup) == 0:
            for i in range(len(data_tup)):
                dic = {}
                # 获取字段名
                for index in range(len(fields)):
                    key = fields[index][0]
                    value = data_tup[i][index]
                    dic[key] = value
                result_list.append(dic)
    except Exception as error:
        print(error)
    cursor.close()
    return result_list


# 增加数据
def insert_info(db, sql_str):
    # 获取游标
    cursor = db.cursor()
    result = 0
    try:
        # 执行sql语句
        result = cursor.execute(sql_str)
        # 提交到数据库执行
        db.commit()
    except Exception as error:
        print('insertError:{}'.format(error))
        # Rollback in case there is any error
        db.rollback()
    # 关闭数据库连接
    cursor.close()
    return result


# 删除数据
def delete_info(db, sql_str):
    # 获取游标
    cursor = db.cursor()
    result = 0
    try:
        # 执行sql语句
        result = cursor.execute(sql_str)
        # 提交到数据库执行
        db.commit()
    except BaseException as error:
        print(error)
        # Rollback in case there is any error
        db.rollback()
    # 关闭数据库连接
    cursor.close()
    return result


# 更新数据
def update_info(db, sql_str):
    # 获取游标
    cursor = db.cursor()
    result = 0
    try:
        # 执行sql语句
        result = cursor.execute(sql_str)
        # 提交到数据库执行
        db.commit()
    except BaseException as error:
        print(error)
        # Rollback in case there is any error
        db.rollback()
    # 关闭数据库连接
    cursor.close()
    return result
