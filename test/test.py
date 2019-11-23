# encoding:utf-8

import json
from param import Data, Body, Json
from url import Request
from utils import Logger
from urllib3.response import HTTPResponse

# if __name__ == '__main__':
#   p = Data('param')
#   b = Body('one', 'two')
#   request = Request()
#   log = Logger().logger
#
#   url = 'http://localhost:8080/test'
#   res: HTTPResponse = request.put(url, b, **p.__dict__)
#   log.info(res.data)

if __name__ == '__main__':
  f = open('test.json', 'r')
  data = f.read()
  clazz: Json = json.loads(data, object_hook = Json.from_dict)
  print(clazz.body.two)
