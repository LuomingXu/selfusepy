import selfusepy
from jsonparse import BaseJsonObject
from selfusepy.utils import override_str
from typing import List


@override_str
class Point(BaseJsonObject):

  def __init__(self):
    self.x: int = -1
    self.demo: Point.Demo = Point.Demo()

  @override_str
  class Demo(BaseJsonObject):
    def __init__(self):
      self.y: int = -1
      self.demo1: List[Point.Demo.Demo1] = [Point.Demo.Demo1()]

    class Demo1(BaseJsonObject):
      def __init__(self):
        self.z: int = -1


def serialize_instance(obj):
  d = {'__classname__': type(obj).__name__}
  d.update(vars(obj))
  return d


classes = {}


def deserialize_object(d):
  cls = d.pop('__classname__', None)
  if cls:
    cls = classes[cls]
    obj = cls.__new__(cls)  # Make instance without calling __init__
    for key, value in d.items():
      setattr(obj, key, value)
    return obj
  else:
    return d


if __name__ == '__main__':
  # s = 'dsfJLKkk'
  # print(upper_first_letter(s))
  # p = Point(1, 2, Demo(3))
  # s = json.dumps(p, default = serialize_instance)
  # print(s)
  # p = Point()
  # cls = type(p.p)
  # cls .__new__(cls)
  # print(cls)
  # print(type(getattr(p, 'p')))
  #
  # test(Point())
  #
  # print(classes)
  # print(classes.pop('Demo1'))

  # test = eval(type(dskfj).__name__ + '()')
  # print('test: %s' % (test.__str__()))

  p: Point = selfusepy.parse_json(open('test.json', 'r').read(), Point())

  print(p)


  # f = open('test.json', 'r')
  # s = f.read()
  # obj: Point = selfusepy.parse_json(s, Point())
  # print(obj)

  # p: Point = json.loads(add_classname(json.loads(s), 'Point'), object_hook = deserialize_object)
  # print(p.demo)
  #
  # f = open('test.json', 'r')
  # s = f.read()
  # p1 = json.loads(s, object_hook = Point.unserialize_object)
  # print(p1)
