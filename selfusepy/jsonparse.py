#   Copyright 2018-2019 LuomingXu
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  Author : Luoming Xu
#  File Name : jsonparse.py
#  Repo: https://github.com/LuomingXu/selfusepy

"""
用来Json to Object的工具库,
可直接在__init__直接调用此工具库的实现
来直接使用
"""
from typing import List

from selfusepy.utils import upper_first_letter

class_dict = {}

__classname__: str = '__classname__'


class BaseJsonObject(object):
  """
  用于在用户自定义Json的转化目标类的基类
  以是否为此基类的子类来判断这个类是否需要转化
  """
  pass


def JSONField(var_key: dict):
  def variableName_to_jsonKey(cls):
    class NoUseClass(object):
      def __init__(self, *args, **kwargs):
        pass

      @classmethod
      def key(cls, k: str):
        return var_key.get(k)

    return NoUseClass

  return variableName_to_jsonKey


def deserialize_object(d: dict) -> object:
  """
  用于json.loads()函数中的object_hook参数
  :param d: json转化过程中的字典
  :return: object
  """
  cls = d.pop(__classname__, None)
  if cls:
    cls = class_dict[cls]
    obj = cls.__new__(cls)  # Make instance without calling __init__
    for key, value in d.items():
      setattr(obj, key, value)
    return obj
  else:
    return d


def add_classname(d: dict, classname: str) -> dict:
  """
  给json字符串添加一个"__classname__"的key来作为转化的标志
  :param d: json的字典
  :param classname: 转化的目标类
  :return: 修改完后的json字符串
  """
  d[__classname__] = classname
  for k, v in d.items():
    if isinstance(v, dict):
      add_classname(v, upper_first_letter(k))
    elif isinstance(v, List):
      for item in v:
        add_classname(item, upper_first_letter(k))

  return d


def add_classname_list(l: list, classname: str) -> list:
  for d in l:
    add_classname(d, classname)
  return l


def generate_class_dict(obj: BaseJsonObject):
  """
  构造需要转化的目标类的所包含的所有类
  将key: 类名, value: class存入class_dict中
  :param obj: 目标类
  """
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
