import json
from typing import TypeVar
from jsonparse import generate_class_dict, add_classname, deserialize_object, class_dict

T = TypeVar('T')


def parse_json(j: str, obj: T) -> T:
  """
  json to Py object
  :param j: json string
  :param obj: Py Object
  :return: obj
  """
  generate_class_dict(obj)
  json_dict: dict = json.loads(j)
  j_modified: str = add_classname(json_dict, type(obj).__name__)
  obj = json.loads(j_modified, object_hook = deserialize_object)

  class_dict.clear()
  return obj
