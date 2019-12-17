#  The Apache License Version 2.0
#  Copyright (c) 2019
#  Author : Luoming Xu
#  Project Name : selfusepy
#  File Name : utils.py
#  CreateTime: 2019/11/26 20:45

import logging, sys, os
from logging import handlers
from typing import MutableMapping


def override_str(clazz):
  """
  override default func __str__(), print Object like Java toString() style
  """

  def __str__(self):
    values: MutableMapping = {}
    for k, v in vars(self).items():
      if isinstance(v, list):
        values[k] = '[%s]' % ', '.join('%s' % item.__str__() for item in v)
      else:
        values[k] = v.__str__()

    return '%s(%s)' % (
      type(self).__name__,  # class name
      ', '.join('%s: %s' % item for item in values.items())
    )

  clazz.__str__ = __str__
  return clazz


class ShowProcess(object):
  """
  显示处理进度的类
  调用该类相关函数即可实现处理进度的显示
  # 效果为[>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>]100.00%
  """

  i = 0  # 当前的处理进度
  max_steps = 0  # 总共需要处理的次数
  max_arrow = 50  # 进度条的长度
  infoDone = 'done'

  def __init__(self, max_steps, infoDone = 'Done'):
    """
    初始化函数，需要知道总共的处理次数
    :param max_steps: 总共需要处理的次数
    :param infoDone: 结束时打印的字符
    """
    self.max_steps = max_steps
    self.i = 0
    self.infoDone = infoDone

  def show_process(self, i = None):
    """
    显示函数，根据当前的处理进度i显示进度
    :param i: 当前进度
    """
    if i is not None:
      self.i = i
    else:
      self.i += 1
    num_arrow = int(self.i * self.max_arrow / self.max_steps)  # 计算显示多少个'>'
    num_line = self.max_arrow - num_arrow  # 计算显示多少个'-'
    percent = self.i * 100.0 / self.max_steps  # 计算完成进度，格式为xx.xx%
    process_bar = '[' + '>' * num_arrow + '-' * num_line + ']' \
                  + '%.2f' % percent + '%' + '\r'  # 带输出的字符串，'\r'表示不换行回到最左边
    sys.stdout.write(process_bar)  # 这两句打印字符到终端
    sys.stdout.flush()
    if self.i >= self.max_steps:
      self.close()

  def close(self):
    print('')
    print(self.infoDone)
    self.i = 0


class Logger(object):
  """
  日志类
  usage: log = Logger('error.log').logger OR log = Logger().logger
         log.info('info')
  """

  def __init__(self, filename = None, when = 'D', backCount = 3,
               fmt = '%(asctime)s - [%(levelname)8s] - [%(threadName)20s] %(pathname)30s.%(funcName)s[line(%(lineno)d)]: %(message)s'):
    """
    init
    :param filename: 储存日志的文件, 为None的话就是不储存日志到文件
    :param when: 间隔的时间单位. S秒, M分, H小时, D天, W每星期(interval==0时代表星期一) midnight 每天凌晨
    :param backCount: 备份文件的个数, 如果超过这个个数, 就会自动删除
    :param fmt: 日志格式
    """
    self.logger = logging.getLogger(filename)
    format_str = logging.Formatter(fmt)
    self.logger.setLevel(logging.DEBUG)  # 设置日志级别为debug, 所有的log都可以打印出来
    sh = logging.StreamHandler()  # 控制台输出
    sh.setFormatter(format_str)
    self.logger.addHandler(sh)
    self.logger.addFilter(LoggerFilter())

    if filename is not None:
      """实例化TimedRotatingFileHandler"""
      th = handlers.TimedRotatingFileHandler(filename = filename, when = when, backupCount = backCount,
                                             encoding = 'utf-8')
      th.setFormatter(format_str)  # 设置文件里写入的格式
      self.logger.addHandler(th)


def upper_first_letter(s: str) -> str:
  """
  make first letter upper case
  :param s:
  :return:
  """
  return s[0].capitalize() + s[1:]


class LoggerFilter(logging.Filter):
  def filter(self, record: logging.LogRecord):
    s = str(record.pathname).replace('\\', '/') .replace(RootPath().rootPath, '').replace('/', '.')[1:]
    if s.__len__() > 30:  # 如果超出了长度再进行缩减操作
      l: list = s.split('.')
      for i, item in enumerate(l):
        if i != l.__len__() - 1:  # 最后一个文件名不进行长度判断
          s = str(item)
          if s.__len__() > 10:  # 对过长的包名进行缩减
            s = s.replace('_', '')  # 如果是以'_'开头的, 需要删去, 才能取首字母
            l[i] = s[0]

      s = '.'.join('%s' % item for item in l)

    record.pathname = s
    return True


class RootPath(object):
  """获取根目录"""

  def __init__(self):
    # 判断调试模式
    debug_vars = dict((a, b) for a, b in os.environ.items()
                      if a.find('IPYTHONENABLE') >= 0)

    # 根据不同场景获取根目录
    if len(debug_vars) > 0:
      """当前为debug运行时"""
      self.rootPath = sys.path[2]
    elif getattr(sys, 'frozen', False):
      """当前为exe运行时"""
      self.rootPath = os.getcwd()
    else:
      """正常执行"""
      self.rootPath = sys.path[1]

    # 替换斜杠
    self.rootPath = self.rootPath.replace('\\', '/')

  def getPathFromResources(self, fileName):
    """按照文件名拼接资源文件路径"""
    filePath = "%s/resources/%s" % (self.rootPath, fileName)
    return filePath
