from apscheduler.schedulers.background import BackgroundScheduler

from src.http_request import http_request
from src.get_resource import everyday_src
import src


if __name__ == "__main__":
    # 初始化配置文件
    src.config.init()

    # 早上
    http_request.good_morning()
    # # 下午
    # http_request.good_afternoon()

    # 每天定时下载资源
    scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
    scheduler.add_job(everyday_src.start, 'interval', days=1, start_date='2022-03-01 00:05:05',
                      end_date='2024-01-01 00:00:00', args=[])
    scheduler.start()

    # 开启接口
    http_request.start()
