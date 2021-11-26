# 返回结果model
def dic_format(code='200', msg='', data=None):
    dic = {
        'code': code,
        'msg': msg,
        'data': data
    }
    return dic
