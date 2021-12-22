# 注册推送
from . import mysql_use


def register_notification(user_id, push_token, alias, registration_id):
    sql = 'INSERT INTO notification(user_id, push_token, alias, registration_id) VALUES (\'{}\',\'{}\',\'{}\',\'{}\')'.format(
        user_id,
        push_token, alias, registration_id)
    print('sql=' + sql)
    cnn = mysql_use.connect_sql()
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
    return res