from functools import partial
from loguru import logger
import sys

__all__ = ['logger']


# 库开发
_DEV_LOGGER = logger.bind(env="dev")


# 默认
# DEBUG：10
# INFO：20
# WARNING：30
# ERROR：40
# CRITICAL：50


# DEV：9
logger.level("DEV", no=9, color="<magenta>")  # 自定义最低等级
logger.level("ROUND", no=9, color="<green>")  # 完成一轮发送并接收到回复
logger.level("PING", no=9, color="<blue>")  # ping
logger.level("PONG", no=9, color="<cyan>")  # pong
logger.level("Q_EVENT", no=9, color="<magenta>")  # 调度事件 Q队列
logger.level("Q_SEND", no=9, color="<magenta>")  # Q队列发送

# DEBUG：10
logger.level("SEND", no=10, color="<green>")  # 发送信息
logger.level("RECV", no=10, color="<magenta>")  # 接收信息

# 19 用户输出
logger.level("PRINT", no=19, color="<white>")  # 用户输出

# INFO：20
logger.level("NOTICE", no=20, color="<green>")  # 通知
logger.level("WOKE", no=20, color="<green>")  # 唤醒
logger.level("CONN", no=20, color="<green>")  # 连接


def format_record_of_cmd(env:str,record):
    """
    自定义日志格式
    """    
    # print(record['file'])
    if record["level"].name == "NOTICE":
        return "<level>{message}</level>\n"
    
    if record["level"].name == "PRINT":
        return "<level>{level: <8}</level>: <level>{name}:{function}:{line}</level> : - {message}\n"
    
    if env == "dev":
        return "<level>{level: <8}</level>: <green>{time:HH:mm:ss}</green>  | <cyan>{name}:{function}:{line: <4}</cyan> : - {message}\n"
    else:
        return "<level>{level: <8}</level>: - {message}\n" 



# 初始化开发环境日志
def init_dev_logger():
    
    current_level = "DEV"  # DEV、DEBUG、INFO、WARNING、ERROR、CRITICAL
    # format="<green>{time:HH:mm:ss}</green> | {time:{elapsed}} | <level>{level: <8}</level> | <cyan>{name}:{function}:{line}</cyan> - <level>{message}</level>"
    logger.remove()  # 移除默认处理器
    logger.add(sys.stdout, level=current_level,format=partial(format_record_of_cmd,"dev"))  # 输出到控制台
    logger.level(current_level)




# 初始化生产环境日志
def init_prod_logger(is_debug=False,*,output_folder: str|None =None, filename:str|None=None):
    
    cmd_level = "PRINT" if is_debug else "WARNING"  # 命令行日志级别 # DEV、DEBUG、PRINT、INFO、WARNING、ERROR、CRITICAL
    # cmd_format="<level>{level: <10}:</level>{message}"  # 命令行日志格式
    
    file_level = "INFO"  # 文件日志级别 # DEV、DEBUG、INFO、WARNING、ERROR、CRITICAL
    file_log_format="<level>{level: <8}</level>: <level>{time:YYYY-MM-DD HH:mm:ss.SSS} | {name}:{function}:{line} - {message}</level>"  # 文件日志格式
    
    logger.level(cmd_level)
    logger.remove()  # 移除默认处理器
    logger.add(sys.stdout, level=cmd_level, format=partial(format_record_of_cmd,"prod"))  # 输出到控制台
    
    if output_folder:  # 输出到文件
        import os
        filename = filename or "utran_log_{time}.log"
        log_file_path = os.path.join(output_folder, filename)  # 拼接完整的文件路径
        logger.add(log_file_path, rotation="500 MB", level=file_level, format=file_log_format) 
    
    # 禁用exception输出
    def _no_exception(*args, **kwargs):...
    setattr(logger, "exception", _no_exception) 




init_dev_logger()


if __name__ == '__main__':    
    # init_prod_logger(True,output_folder='.')
    
    logger.debug('This is a debug message')
    logger.info('This is an info message,<red>red</red>')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')
    logger.success("ok")
    logger.log("NOTICE","notice")
    logger.log("PRINT","print")
    
    import logging
    logger.log("INFO", "info, \033[31m{color}\033[0m".format(color="red"))

    logger.log("ROUND","round",'sdfsdf')
    from functools import partial
    
    fn = partial(lambda *args:partial(logger.log,"PRINT",''.join(args))())
    
    fn("test","test2")
    try:
        a = 1 / 0
    except Exception as e:
        logger.exception(e)
