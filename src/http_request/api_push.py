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

    # 插入数据表
    sql = 'INSERT INTO notification(user_id, push_token, alias, registration_id, identifier) VALUES (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'.format(
        user_id,
        push_token, alias, registration_id, identifier)
    res = mysql_use.insert_info(cnn, sql)
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
def push_alias(alias, alert, title=None):
    if push.jpush is None:
        push.init()

    push.alias(alias, alert=alert, title=title)
    # 消息添加到数据库
    sql = 'INSERT INTO message(title, content, type, alias) VALUES (\'{}\',\'{}\',\'{}\',\'{}\')'.format(title, alert,
                                                                                                         2, alias)
    print(alias)
    cnn = mysql_use.connect_sql()
    mysql_use.insert_info(cnn, sql)
    cnn.close()


# 推送全部
def push_all(alert='', title='nothing', save_title=None, save_content=None, push_type=1):
    if push.jpush is None:
        push.init()
    push.push_all(alert=alert, title=title)

    # 保存的标题和内容
    if save_title is None:
        save_title = title
    if save_content is None:
        save_content = alert

    # 消息添加到数据库
    sql = 'INSERT INTO message(title, content, type) VALUES (\'{}\',\'{}\',\'{}\')'.format(save_title, save_content,
                                                                                           push_type)
    cnn = mysql_use.connect_sql()
    mysql_use.insert_info(cnn, sql)
    cnn.close()


# 获取推送消息
def get_messages(alias=None):
    sql = "select * FROM  message where alias like \'%{}%\' or type = 1 and hide = 0 order by date DESC".format(
        alias)
    cnn = mysql_use.connect_sql()
    res = mysql_use.search_info(cnn, sql)
    return res


# 删除消息
def delete_messages(id):
    sql = mysql_use.updateSqlStr('message', {'hide': '1'}, {'id': id})
    cnn = mysql_use.connect_sql()
    res = mysql_use.update_info(cnn, sql)
    return res
