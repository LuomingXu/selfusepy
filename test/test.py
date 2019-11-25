import json


class Demo(object):
  def __init__(self):
    self.y: int = -1


class Point(object):

  def unserialize_object(d: dict):
    for key, value in d.items():
      cls = type(getattr(Point(), key))
      obj = cls.__new__(cls)
      setattr(obj, key, value)
    return obj

  def __demo__(self):
    for item in vars(self):
      cls = type(getattr(self, item))
      try:
        print('item: %s, class: %s' % (item, cls))
        obj = eval(cls())
        print('')
        print(vars(obj))
      except BaseException as e:
        pass

  def __init__(self):
    self.x: int = -1
    self.demo: Demo = Demo()

    self.__demo__()


classes = {
  'Point': Point,
  'Demo': Demo
}


def serialize_instance(obj):
  d = {'__classname__': type(obj).__name__}
  d.update(vars(obj))
  return d


def unserialize_object(d):
  clsname = d.pop('__classname__', None)
  if clsname:
    cls = classes[clsname]
    obj = cls.__new__(cls)  # Make instance without calling __init__
    for key, value in d.items():
      setattr(obj, key, value)
    return obj
  else:
    return d


if __name__ == '__main__':
  # p = Point(1, 2, Demo(3))
  # s = json.dumps(p, default = serialize_instance)
  # print(s)
  # p = Point()
  # cls = type(p.p)
  # cls .__new__(cls)
  # print(cls)
  # print(type(getattr(p, 'p')))
  print(vars(Point.__new__(Point)))
  dskfj = Point()
  # f = open('demo.json', 'r')
  # s = f.read()
  # p = json.loads(s, object_hook = unserialize_object)
  #
  # f = open('test.json', 'r')
  # s = f.read()
  # p1 = json.loads(s, object_hook = Point.unserialize_object)
  # print(p1)
