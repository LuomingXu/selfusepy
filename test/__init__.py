import unittest

import jsontest
import log.package
import log.package.package
import log.package.package.package


class TestCase(unittest.TestCase):
  def test_jsonparse(self):
    self.assertEqual(jsontest.json_test_1(), True)
    self.assertEqual(jsontest.json_test_2(), True)
    self.assertEqual(jsontest.json_test_3(), (True, True))
    self.assertEqual(jsontest.json_test_4(), True)


if __name__ == '__main__':
  log.log_test()
  log.package.log_test()
  log.package.package.log_test()
  log.package.package.package.log_test()
  unittest.main()
