import config
from src.http_request import http_request, api_push
import src

if __name__ == "__main__":
    # 初始化配置文件
    src.config.init()

    api_push.push_alias(alias='biubiubiu', alert='alert', title='title')

    # http_request.good_morning()
    # http_request.good_afternoon()

    http_request.start()



