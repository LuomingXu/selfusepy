import selfusepy
from typing import List
from selfusepy.jsonparse import BaseJsonObject
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


def json_test_1():
  """
  json test
  e.g. 1
  """
  print('多级复杂json转化测试: ')
  f = open('./jsontest/eg1.json', 'r')
  obj: One = selfusepy.parse_json(f.read(), One())
  print(obj)


def json_test_2():
  """
  json test with jsonarray
  e.g. 2
  """
  print('包含json array的转化测试: ')
  f = open('./jsontest/eg2.json', 'r')
  obj: One1 = selfusepy.parse_json(f.read(), One1())
  print(obj)


def json_test_3():
  """
  json test, parse jsonArrary
  e.g. 3
  """
  print('json array测试: ')
  f = open('./jsontest/eg3.json')
  l: List[One] = selfusepy.parse_json_arrary(f.read(), One())
  for i, item in enumerate(l):
    print('i: %s, value: %s' % (i, item))
