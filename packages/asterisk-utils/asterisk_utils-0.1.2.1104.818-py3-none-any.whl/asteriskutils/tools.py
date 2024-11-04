
from colorama import init
import logging.config,datetime

# 解决Window环境中打印颜色问题
init(autoreset=True)


def get_logger()-> logging.Logger:
    '''
    根据AppConfig设置log基本配置，并返回logger对象
    Returns
        logger: 日志实例
    '''
    from asteriskutils.setting import AppConfig
    
    import os
    # 根据AppConfig的设置拼接日志文件名
    fn = '{}.log'.format(datetime.datetime.now().strftime(AppConfig['log']['log_file_name']))
    # 使用join的目的是适配不同操作系统
    # 载入日志的配置文件
    logging.config.fileConfig(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log.config'))
    logger = logging.getLogger('MainLogger')
    try:
        fh = logging.FileHandler(os.path.join(os.path.abspath(os.curdir),AppConfig['log']['log_path'],fn),'a','utf-8')
    except FileNotFoundError:
        try:
            os.mkdir(os.path.join(os.path.abspath(os.curdir),AppConfig['log']['log_path']))
            fh = logging.FileHandler(os.path.join(os.path.abspath(os.curdir),AppConfig['log']['log_path'],fn) )
        except:
            print("\033[31m无法创建日志文件目录，请在调用log前，覆盖设置设置AppConfig['log']['log_path']到项目目录.\033[0m")   
            raise FileNotFoundError
        
    fh.setFormatter(logging.Formatter(AppConfig['log']['log_format']))
    logger.addHandler(fh)
    return logger


def success_print(txt,header=True,*args,**kwargs) -> None:
    '''
    成功信息打印，绿色
    Args
        txt(str):需要在屏幕输出的文字
        header(bool):是否打印开头的[成功信息]
        args(list):其他print的参数
        kwargs(dict):其他print的参数
    '''
    s = '[成功信息]' if header else ''
    print(f'\033[32m{s}{txt}\033[0m',*args,**kwargs)
    get_logger().info(f'{s}{txt}')
def error_print(txt,header=True,*args,**kwargs):
    '''
    错误信息打印，红色
    Args
        txt(str):需要在屏幕输出的文字
        header(bool):是否打印开头的[成功信息]
        args(list):其他print的参数
        kwargs(dict):其他print的参数
    '''
    s = '[错误信息]' if header else ''
    print(f'\033[31m{s}{txt}\033[0m',*args,**kwargs)
    get_logger().error(f'{s}{txt}',exc_info=True, stack_info=True,)

def iprint(txt,header:str='运行信息',*args,**kwargs) -> None:
    '''
    输出信息打印，蓝色
    Args
        txt(str):需要在屏幕输出的文字
        header(str):是否打印开头的[运行信息]
        args(list):其他print的参数
        kwargs(dict):其他print的参数
    '''
    s = f'[{header}]' if header else ''
    print(f'\033[36m{s}{txt}\033[0m',*args,**kwargs)
    if header:
        get_logger().info(f'{s}{txt}')
def wprint(txt:str,header:str='警告信息',*args,**kwargs) -> None:
    '''
    警告信息打印，黄色
    Args
        txt(str):需要在屏幕输出的文字
        header(str):是否打印开头的[警告信息]的文字，默认为'警告信息'
        args(list):其他print的参数
        kwargs(dict):其他print的参数
    '''
    s = f'[{header}]:' if header else ''
    print(f'\033[33m{s}{txt}\033[0m',*args,**kwargs)
    get_logger().warning(f'{s}{txt}')

def dprint(txt,header:str='调试信息',*args,**kwargs) -> None:
    '''
    当配置文件中AppConfig的debug属性为true时打印，否则不打印
    按照以下格式:
    [调试信息] [{参数名/函数名}] :{value}
    Args
        txt(str):需要在屏幕输出的文字
        header(str):是否打印开头的[调试信息]
        args(list):其他print的参数
        kwargs(dict):其他print的参数
    '''
    from asteriskutils.setting import AppConfig
    import inspect
    if AppConfig['debug']:
        s = f"[{header}]:" if header else ''
        txt_name = 'Unknown' # 默认值
        txt_name = inspect.stack()[1][4][0].split("(")[1].split(")")[0] # 获取参数名称或者函数名称        
        print(f'\033[35m{s}[{txt_name}] => {txt}\033[0m',*args,**kwargs)
        get_logger().debug(f'{s}[{txt_name}] => {txt}')