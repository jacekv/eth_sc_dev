import unittest
import sys
import logging
import inspect

sys.path.append("../eth/")
from evm import EVM
from evm import State
from executionEnvironment import ExecutionEnvironment

class EVMLogicTest(unittest.TestCase):

    def setUp(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)
        self.evm = EVM(logger=logger)

    def testIsZeroTrue(self):
        code = '603315'
        self.execCode(code, 0x0)

    def testIsZeroTrue(self):
        code = '600015'
        self.execCode(code, 0x01)

    def testAnd1(self):
        code = '6011603316'
        self.execCode(code, 0x11)

    def testAnd2(self):
        code = '6011602216'
        self.execCode(code, 0x00)

    def testOr1(self):
        code = '6011603317'
        self.execCode(code, 0x33)

    def testOr2(self):
        code = '6011602217'
        self.execCode(code, 0x33)

    def testXor(self):
        code = '60037Fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff9c18'
        self.execCode(code, 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff9f)

    def testNot(self):
        code = '7Fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff9c19'
        self.execCode(code, 0x63)

    def testNot2(self):
        code = '606319'
        self.execCode(code, 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff9c)

    def execCode(self, code, assertValue):
        environment = ExecutionEnvironment(code)
        #self.evm.setCode(code)
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), assertValue)


    def runTest(self):
        methods = dir(self)
        for method in methods:
            if method[:4] == 'test':
                getattr(self, method)()


if __name__ == '__main__':
    unittest.main()
