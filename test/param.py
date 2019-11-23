# encoding:utf-8

from utils import override_str, EnableJsonInterface


@override_str
class Data(object):

  def __init__(self, param):
    self.param = param


@override_str
class Body(object):

  def __init__(self):
    self.one: str
    self.two: str


@override_str
class Json(EnableJsonInterface):

  # @classmethod
  # def from_dict(clz, dict):
  #   obj = clz()
  #   obj.__dict__.update(dict)
  #   return obj

  def __init__(self):
    self.one: int = -1
    self.two: int = -1
    self.body: Json.Body = None

  class Body(object):

    def __init__(self):
      self.one: str = ''
      self.two: str = ''
