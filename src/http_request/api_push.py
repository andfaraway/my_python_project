# 注册推送
from . import mysql_use
from . import push


# 注册推送
def register_notification(**kwargs):
    user_id = kwargs.get('user_id')
    push_token = kwargs.get('push_token')
    alias = kwargs.get('alias')
    registration_id = kwargs.get('registration_id')
    identifier = kwargs.get('identifier')

    cnn = mysql_use.connect_sql()
    # 查询是否注册
    sql = "select * FROM  notification where identifier = \'{}\'".format(identifier)
    print('sql=' + sql)
    res = mysql_use.search_info(cnn, sql)
    # 未注册，注册
    if len(res) == 0:
        sql = 'INSERT INTO notification(user_id, push_token, alias, registration_id, identifier) VALUES (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'.format(
            user_id,
            push_token, alias, registration_id, identifier)
        print('未注册，注册sql=' + sql)
        res = mysql_use.insert_info(cnn, sql)
    else:
        # 已注册，更新
        sql = 'UPDATE notification SET user_id = \'{}\',push_token = \'{}\',alias = \'{}\',registration_id = \'{}\' WHERE identifier = \'{}\''.format(
            user_id,
            push_token, alias, registration_id, identifier)
        print('已注册，更新sql=' + sql)
        res = mysql_use.update_info(cnn, sql)
    cnn.close()
    return res


# 获取推送别名
def get_alias():
    sql = "select alias FROM  notification"
    print('sql=' + sql)
    cnn = mysql_use.connect_sql()
    res = mysql_use.search_info(cnn, sql)
    cnn.close()

    alias = []
    for dic in res:
        alia = dic['alias']
        alias.append(alia)
    return alias


# 按别名推送
def push_alias(alias, alert):
    push.alias(alias, alert=alert)
