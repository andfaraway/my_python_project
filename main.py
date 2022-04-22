from apscheduler.schedulers.background import BackgroundScheduler

from http_request import http_request
from src.get_resource import desktop_images, get_source_to_sql
from src.get_resource import everyday_src
import src

if __name__ == "__main__":
    # 初始化配置文件
    src.config.init()

    http_request.good_morning()
    # 下午
    # http_request.good_afternoon()

    # 每天定时下载资源
    scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
    scheduler.add_job(everyday_src.start, 'interval', days=1, start_date='2022-03-01 00:00:05',
                      end_date='2024-01-01 00:00:00', args=[])
    scheduler.start()

    # 开启接口
    http_request.start()
