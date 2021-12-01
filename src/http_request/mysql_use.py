import pymysql
import re


# 打开数据库连接
def connect_sql():
    host = '1.14.252.115'
    user = 'root'
    passwd = 'lbsmysql'
    db = 'nothing'

    conn = pymysql.connect(host=host, user=user, passwd=passwd, )
    conn.select_db(db)
    return conn


# 查询数据库数据
def search_info(db, sql_str):
    # 获取游标
    cursor = db.cursor()
    result = 0
    dic = {}
    try:
        # 获取查询结果元组
        result = cursor.execute(sql_str)
        data_tup = cursor.fetchall()
        if not len(data_tup) == 0:
            # 获取字段名
            fields = cursor.description
            print(data_tup)
            for index in range(len(fields)):
                key = fields[index][0]
                value = data_tup[0][index]
                dic[key] = value
    except Exception as error:
        print(error)

    cursor.close()
    db.close()
    return [result, dic]


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
    except BaseException as error:
        print(error)
        # Rollback in case there is any error
        db.rollback()
    # 关闭数据库连接
    cursor.close()
    db.close()
    return [result]


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
    db.close()
    return [result]


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
    db.close()
    return [result]
