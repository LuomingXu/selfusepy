# encoding:utf-8

import sys, logging
from logging import handlers


def override_str(clz):
  """
  override default func __str__(), print Object like Java toString() style
  """

  def __str__(self):
    return '%s[%s]' % (
      type(self).__name__,  # class name
      ', '.join('%s: %s' % item for item in vars(self).items())
    )

  clz.__str__ = __str__
  return clz


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

  # 初始化函数，需要知道总共的处理次数
  def __init__(self, max_steps, infoDone = 'Done'):
    self.max_steps = max_steps
    self.i = 0
    self.infoDone = infoDone

  # 显示函数，根据当前的处理进度i显示进度
  def show_process(self, i = None):
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
  usage: log = Logger('error.log').logger
         log.info('info')
  """

  def __init__(self, filename = None, when = 'D', backCount = 3,
               fmt = '%(asctime)s - [%(levelname)8s] - [%(threadName)20s] %(module)10s.%(funcName)s - %(filename)s[line:%(lineno)d] : %(message)s'):
    self.logger = logging.getLogger(filename)
    format_str = logging.Formatter(fmt)
    self.logger.setLevel(logging.DEBUG)  # 设置日志级别为debug, 所有的log都可以打印出来
    sh = logging.StreamHandler()  # 控制台输出
    sh.setFormatter(format_str)
    self.logger.addHandler(sh)

    if filename is not None:
      th = handlers.TimedRotatingFileHandler(filename = filename, when = when, backupCount = backCount,
                                             encoding = 'utf-8')
      # 实例化TimedRotatingFileHandler
      # backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
      # S秒, M分, H小时, D天, W每星期(interval==0时代表星期一) midnight 每天凌晨
      th.setFormatter(format_str)  # 设置文件里写入的格式
      self.logger.addHandler(th)
