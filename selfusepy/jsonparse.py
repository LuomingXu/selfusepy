from typing import List
from utils import upper_first_letter

class_dict = {}

__classname__: str = '__classname__'


class BaseJsonObject(object):
  pass


class JsonParseError(Exception):
  def __init__(self, msg):
    super().__init__(self)
    self.msg = msg

  def __str__(self) -> str:
    return self.msg


def deserialize_object(d: dict) -> object:
  cls = d.pop(__classname__, None)
  if cls:
    cls = class_dict[cls]
    obj = cls.__new__(cls)  # Make instance without calling __init__
    for key, value in d.items():
      setattr(obj, key, value)
    return obj
  else:
    return d


def add_classname(d: dict, classname: str) -> str:
  d[__classname__] = classname
  for k, v in d.items():
    if isinstance(v, dict):
      add_classname(v, upper_first_letter(k))
    elif isinstance(v, List):
      for item in v:
        add_classname(item, upper_first_letter(k))

  return d.__str__().replace('\'', '\"')


def generate_class_dict(obj: BaseJsonObject):
  cls = type(obj)
  class_dict[cls.__name__] = cls
  for item in vars(obj).values():
    cls = type(item)
    if issubclass(cls, BaseJsonObject):
      generate_class_dict(cls())
    elif issubclass(cls, List):
      cls = type(item.pop(0))
      if issubclass(cls, BaseJsonObject):
        generate_class_dict(cls())
