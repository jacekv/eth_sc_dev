import unittest

from testEVMSimplePUSH import EVMPushTest
from testEVMSimpleArithmetic import EVMArithmeticTest
from testEVMSimpleLogic import EVMLogicTest

def suite():
    suite = unittest.TestSuite()
    suite.addTest(EVMPushTest())
    suite.addTest(EVMArithmeticTest())
    suite.addTest(EVMLogicTest())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite())
