import os
import logging
import logging.config
from conf import log_settings,settings


def load_my_logging_cfg(name):

    logfile_name = f'{name}.log'
    logfile_path = os.path.join(settings.LOG_PATH, logfile_name)
    log_settings.LOGGING_DIC['handlers']['default']['filename'] = logfile_path

    logging.config.dictConfig(log_settings.LOGGING_DIC)  # 导入上面定义的logging配置
    logger = logging.getLogger(name)  # 生成一个log实例
    logger.info(f'{name} works!')  # 记录该文件的运行状态

    return logger

if __name__ == '__main__':
    load_my_logging_cfg('aaa')
