import unittest
import sys

sys.path.append("eth/")

from testEVMSimplePUSH import EVMPushTest
from testEVMSimpleDUP import EVMDupTest
from testEVMSimpleSWAP import EVMSwapTest

from testEVMSimpleArithmetic import EVMArithmeticTest
from testEVMSimpleLogic import EVMLogicTest
from testEVMSimpleEnvInfo import EVMEnvInfoTest
from testEVMSimpleMemFlow import EVMMemFlowTest


def suite():
    suite = unittest.TestSuite()
    suite.addTest(EVMPushTest())
    suite.addTest(EVMArithmeticTest())
    suite.addTest(EVMLogicTest())
    suite.addTest(EVMDupTest())
    suite.addTest(EVMSwapTest())
    suite.addTest(EVMEnvInfoTest())
    suite.addTest(EVMMemFlowTest())
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite())
