import pymysql

# 读取配置
from src import config


# 打开数据库连接
def connect_sql():
    item = 'mysql'
    host = config.get('host', item)
    user = config.get('user', item)
    passwd = config.get('passwd', item)
    db = config.get('db', item)
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


# 更新数据 0.正常  1.异常
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
        result = 1
    # 关闭数据库连接
    cursor.close()
    return result


# 获取插入sql
# insert_dic:需要插入的字段字典
def insertSqlStr(table, insert_dic):
    keys = list(insert_dic.keys())
    key_str = ''
    value_str = ''
    for index in range(len(keys)):
        key = keys[index]
        value = insert_dic.get(key)
        key_str = key_str + key
        value_str = value_str + '\'{}\''.format(value)

        if index < len(keys) - 1:
            key_str += ','
            value_str += ','

    sql = 'INSERT INTO {}({}) VALUES ({})'.format(table, key_str, value_str)
    return sql


# 获取更新sql
# update_dic:需要更新的字段字典，match：匹配的字段字典
def updateSqlStr(table, update_dic, match_dic):
    # 更改内容
    keys1 = list(update_dic.keys())
    update_str = ''
    for index in range(len(keys1)):
        key = keys1[index]
        value = update_dic.get(key)
        update_str += ' {} = \'{}\' '.format(key, value)

        if index < len(keys1) - 1:
            update_str += ','

    # 匹配条件
    keys2 = list(match_dic.keys())
    match_str = ''
    for index in range(len(keys2)):
        key = keys2[index]
        value = match_dic.get(key)
        match_str = match_str + '{} = \'{}\' '.format(key, value)

        if index < len(keys2) - 1:
            update_str += ' and '

    sql = 'UPDATE {} SET {} WHERE {}'.format(table, update_str, match_str)
    return sql
