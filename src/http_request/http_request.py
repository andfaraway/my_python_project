from flask import Flask, request
from gevent import pywsgi

import mysql_use
import http_result

app = Flask(__name__)


@app.route("/login")
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    if username is None or password is None:
        return http_result.dic_format(code=201, msg='Parameters are missing')

    result_dic = mysql_use.check(username, password)
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


if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()
