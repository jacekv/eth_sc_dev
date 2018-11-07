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

    def testSubstraction(self):
        code = '603361334403'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x3311)

    def runTest(self):
        methods = dir(self)
        for method in methods:
            if method[:4] == 'test':
                getattr(self, method)()


if __name__ == '__main__':
    unittest.main()
