import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
from loguru import logger
from apscheduler.schedulers.blocking import BlockingScheduler
import da_ban.da_ban_service as da_ban_service
from datetime import datetime
import mns_common.utils.date_handle_util as date_handle_util


def auto_da_ban_task():
    logger.info("定时打板任务启动")
    while True:
        try:
            now_date = datetime.now()
            now_str_day = now_date.strftime('%Y-%m-%d')
            if bool(1 - date_handle_util.is_trade_date(now_str_day)):
                logger.info("非交易日不执行:{}", e)
                break
            else:
                # 执行打板任务
                da_ban_service.auto_da_ban()
                hour = now_date.hour
                if hour >= 20:
                    logger.info("超过20点 不在执行:{}", e)

        except BaseException as e:
            logger.error("自动打板定时任务异常:{}", e)


# # 定义BlockingScheduler
blockingScheduler = BlockingScheduler()
# 同步新公告信息
blockingScheduler.add_job(auto_da_ban_task, 'cron', hour='15', minute='37')

logger.info('定时任务启动成功')
blockingScheduler.start()
#
