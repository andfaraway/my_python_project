from flask import Flask, request
from gevent import pywsgi

from . import api
from . import http_result

app = Flask(__name__)


@app.route("/login", methods=['get', 'post'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    if username is None or password is None:
        return http_result.dic_format(code=201, msg='Parameters are missing')

    r_list = api.login(username, password)
    print('r_list = {}'.format(r_list))
    result_dic = r_list[1:]

    return http_result.dic_format(code=200, msg='test', data=get_src())
    if result_dic is None or len(result_dic) == 0:
        return http_result.dic_format(code=203, msg='failure')
    else:
        return http_result.dic_format(code=200, msg='success', data=result_dic)


@app.route("/")
def main_func():
    return "Hello World!"


def start():
    # app.run(host='0.0.0.0')
    _server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    _server.serve_forever()


def get_src():
    import os
    path = os.getcwd()
    path = path.replace('my_python_project', 'default/src/')

    print(path)
    files = os.listdir(path)

    files_list = []
    for file in files:
        if os.path.isdir(path + file):
            files_list.append(file)

    dic = {}
    for dir_name in files_list:
        files = os.listdir(path + dir_name + '/')
        dic[dir_name] = files
    print(dic)
    return dic


if __name__ == "__main__":
    start()
