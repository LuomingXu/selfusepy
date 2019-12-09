import selfusepy, binascii
from typing import List
from jsontest.jsontest import One, One1
from crc32 import crc32DO
from db import engine
from selfusepy.utils import Logger


def json_test_1():
  """
  json test
  e.g. 1
  """
  f = open('./jsontest/eg1.json', 'r')
  obj: One = selfusepy.parse_json(f.read(), One())
  print(obj)


def json_test_2():
  """
  json test with jsonarray
  e.g. 2
  """
  f = open('./jsontest/eg2.json', 'r')
  obj: One1 = selfusepy.parse_json(f.read(), One1())
  print(obj)


if __name__ == '__main__':
  # json_test_1()
  # json_test_2()

  log = Logger().logger
  hashes: List[crc32DO] = []
  conn = engine.connect()
  for i in range(4_4652_0001, 5_0000_0000):
    hashes.append(crc32DO(binascii.crc32(str(i).encode("utf-8")), i))

    if i % 6_0000 == 0:
      log.info('i: %s' % (i))

      sql: str = "insert into crc32(hash, value) values %s" % (', '.join('%s' % item.__str__() for item in hashes))
      hashes.clear()

      try:
        conn.execute(sql)
      except Exception as e:
        log.exception(e)
        exit(0)

      log.info('Done')
