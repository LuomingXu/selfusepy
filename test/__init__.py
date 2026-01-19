import unittest

import jsontest
import logtest.package
import logtest.package.package
import logtest.package.package.package
import logtest.package.package.package.package
import logtest.package.package.package.package.package.longlonglonglonglonglonglonglong

import sys
sys.path.append('./')

class TestCase(unittest.TestCase):
    def test_jsonparse(self):
        self.assertEqual(jsontest.json_test_0(), True)
        self.assertEqual(jsontest.json_test_1(), True)
        self.assertEqual(jsontest.json_test_2(), True)
        self.assertEqual(jsontest.json_test_3(), (True, True))
        self.assertEqual(jsontest.json_test_4(), True)
        self.assertEqual(jsontest.json_test_5(), True)
        self.assertEqual(jsontest.json_test_6(), True)
        self.assertEqual(jsontest.json_test_7(), True)
        self.assertEqual(jsontest.json_test_8(), True)
        self.assertEqual(jsontest.json_test_9(), True)
        self.assertEqual(jsontest.json_test_10(), True)


if __name__ == '__main__':
    logtest.log_test()
    logtest.package.log_test()
    logtest.package.package.log_test()
    logtest.package.package.package.log_test()
    logtest.package.package.package.package.log_test()
    logtest.package.package.package.package.package.longlonglonglonglonglonglonglong.log_test()
    logtest.log_time_test()
    unittest.main()
