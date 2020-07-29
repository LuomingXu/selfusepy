import sys

sys.path.append('..')
sys.path.append('../selfusepy')
sys.path.append('../test')

from typing import List

import selfusepy
from selfusepy.jsonparse import BaseJsonObject, DeserializeConfig, JsonField
from selfusepy.utils import override_str
from datetime import datetime


@override_str
class One(BaseJsonObject):

  def __init__(self):
    self.x: str = ''
    self.two: One.Two = One.Two()

  @override_str
  class Two(BaseJsonObject):
    def __init__(self):
      self.y: str = ''
      self.three: One.Two.Three = One.Two.Three()

    @override_str
    class Three(BaseJsonObject):
      def __init__(self):
        self.z: str = ''


@override_str
class One1(BaseJsonObject):

  def __init__(self):
    self.x: str = ''
    self.two: List[One1.Two] = [One1.Two()]

  @override_str
  class Two(BaseJsonObject):
    def __init__(self):
      self.y: str = ''


@override_str
@DeserializeConfig({'x--': JsonField(varname = 'x')})
class One2(BaseJsonObject):

  def __init__(self):
    self.x: str = ''
    self.two: One2.Two = One2.Two()

  @override_str
  @DeserializeConfig({'y--': JsonField(varname = 'y')})
  class Two(BaseJsonObject):
    def __init__(self):
      self.y: str = ''
      self.three: One2.Two.Three = One2.Two.Three()

    @override_str
    @DeserializeConfig({'z--': JsonField(varname = 'z')})
    class Three(BaseJsonObject):
      def __init__(self):
        self.z: str = ''


@override_str
class One3(BaseJsonObject):
  def __init__(self):
    self.x: str = 'x'
    self.two: List[One3.Two] = [One3.Two()]

  @override_str
  class Two(BaseJsonObject):
    def __init__(self):
      self.y: str = 'y'
      self.three: List[One3.Two.Three] = [One3.Two.Three()]

    @override_str
    class Three(BaseJsonObject):
      def __init__(self):
        self.z: str = 'z'


@override_str
class One4(BaseJsonObject):
  def __init__(self):
    self.x: str = ''
    self.y: List[int] = [0]


def json_test_1() -> bool:
  """
  json test
  e.g. 1
  """
  print('多级复杂json转化测试: ')
  f = open('./jsontest/eg1.json', 'r')
  obj: One = selfusepy.parse_json(f.read(), One())
  print(obj)
  f.close()
  return isinstance(obj, One)


def json_test_2() -> bool:
  """
  json test with jsonarray
  e.g. 2
  """
  print('包含json array的转化测试: ')
  f = open('./jsontest/eg2.json', 'r')
  obj: One1 = selfusepy.parse_json(f.read(), One1())
  print(obj)
  f.close()
  return isinstance(obj, One1)


def json_test_3() -> (bool, bool):
  """
  json test, parse jsonArrary
  e.g. 3
  """
  print('json array测试: ')
  f = open('./jsontest/eg3.json', 'r')
  l: List[One] = selfusepy.parse_json_array(f.read(), One())
  for i, item in enumerate(l):
    print('i: %s, value: %s' % (i, item))
  f.close()
  return isinstance(l, list), isinstance(l.pop(0), One)


def json_test_4() -> bool:
  """
  json test, json-key is different from variable name
  e.g. 3
  """
  print('json不同变量名测试: ')
  f = open('./jsontest/eg4.json', 'r')
  obj: One2 = selfusepy.parse_json(f.read(), One2())
  print(obj)
  f.close()
  return isinstance(obj, One2)


def json_test_5() -> bool:
  print('多级list测试')
  f = open('./jsontest/eg5.json', 'r')
  obj: One3 = selfusepy.parse_json(f.read(), One3())
  print(obj)
  f.close()
  return isinstance(obj, One3)


def json_test_6() -> bool:
  print('线程安全测试')
  f = open('./jsontest/eg1.json', 'r')
  s1 = f.read()
  f.close()
  f = open('./jsontest/eg2.json', 'r')
  s2 = f.read()
  f.close()
  f = open('./jsontest/eg3.json', 'r')
  s3 = f.read()
  f.close()
  from multiprocessing import Pool
  from multiprocessing.pool import ApplyResult
  p = Pool(processes = 3)
  res: List[ApplyResult] = list()
  res.append(p.apply_async(func = selfusepy.parse_json, args = (s1, One(),)))
  res.append(p.apply_async(func = selfusepy.parse_json, args = (s2, One1(),)))
  res.append(p.apply_async(func = selfusepy.parse_json_array, args = (s3, One(),)))
  p.close()
  p.join()
  for item in res:
    value = item.get()
    if isinstance(value, list):
      print('list: ')
      for l in value:
        print(l)
    else:
      print(value)

  return True


def json_test_7() -> bool:
  print("List[int]测试")
  f = open('./jsontest/eg6.json', 'r')
  s = f.read()
  f.close()
  obj: One4 = selfusepy.parse_json(s, One4())

  return isinstance(obj, One4)


def handle(x):
  x = x[0:-1]  # 去除后缀的"Z"
  return datetime.fromisoformat(x)


@override_str
class Obj(BaseJsonObject):

  def __init__(self):
    self.id: Obj.Id = Obj.Id()
    self.client: str = ''
    self.status: Obj.Status = Obj.Status()

  @DeserializeConfig({"$oid": JsonField("oid")})
  class Id(BaseJsonObject):

    def __init__(self):
      self.oid: str = ''

  class Status(BaseJsonObject):

    def __init__(self):
      self.capture_time: Obj.Status.Capture_time = Obj.Status.Capture_time()
      self.cpu_number: int = -1
      self.memory_cap: int = -1
      self.load: int = -1
      self.cpu_usage = -1
      self.memory_usage = -1

    @DeserializeConfig({"$date": JsonField("date", func = handle)})
    class Capture_time(BaseJsonObject):

      def __init__(self):
        self.date: datetime = datetime.now()


def json_test_8() -> bool:
  print("多级; 不同变量名; variable handler")
  with open("./jsontest/eg7.json", "r") as f:
    s = f.read()
  obj: Obj = selfusepy.parse_json(s, Obj())
  return isinstance(obj, Obj)
