import unittest

from testEVMSimplePUSH import EVMPushTest
from testEVMSimpleArithmetic import EVMArithmeticTest

def suite():
    suite = unittest.TestSuite()
    suite.addTest(EVMPushTest())
    suite.addTest(EVMArithmeticTest())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite())
