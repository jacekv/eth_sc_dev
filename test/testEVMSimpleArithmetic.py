import unittest
import sys
sys.path.append("../eth/")
from evm import EVM
import logging
import inspect

class EVMArithmeticTest(unittest.TestCase):

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

    def testAddition(self):
        code = '603361334401'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x3377)

    def testMultiplication(self):
        code = '603361334402'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0xA368C)

    def testSubstraction(self):
        code = '603361334403'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x3311)

    def testDivisionNonZero(self):
        code = '603361334505'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x101)

    def testLtTrue(self):
        code = '603361334510'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x0)

    def testLtFalse(self):
        code = '613345603310'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x01)

    def testGtTrue(self):
        code = '603361334511'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x01)

    def testGtFalse(self):
        code = '613345603311'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x0)

    def testEqFalse(self):
        code = '613345603314'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x0)

    def testEqTrue(self):
        code = '6033603314'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x01)

    def runTest(self):
        methods = dir(self)
        for method in methods:
            if method[:4] == 'test':
                getattr(self, method)()


if __name__ == '__main__':
    unittest.main()
