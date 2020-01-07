from typing import List

import selfusepy
from selfusepy.jsonparse import BaseJsonObject, DeserializeConfig, JsonField
from selfusepy.utils import override_str


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
