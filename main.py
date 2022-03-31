from src.http_request import http_request, api_push
from src.get_resource import desktop_images
import src

if __name__ == "__main__":
    # 初始化配置文件
    src.config.init()

    http_request.good_morning()
    http_request.good_afternoon()
    desktop_images.start()

    http_request.start()



