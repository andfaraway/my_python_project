# 返回结果model
import inspect

from .error_code import *


def dic_format(error_code=ErrorCode.CODE_200, msg=None, data=None):
    if msg is None:
        msg = error_code.msg
    dic = {
        'code': error_code.code,
        'msg': msg,
        'data': data
    }
    return dic


# 判断参数缺失
def request_has_empty(*args):
    for a in args:
        if a is None:
            return True
    return False


def get_variable_name(variable):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [f'{var_name}: {var_val}' for var_name, var_val in callers_local_vars if var_val is variable]
