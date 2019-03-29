import unittest
import sys
sys.path.append("../eth/")
import logging
import inspect

from evm import EVM
from executionEnvironment import ExecutionEnvironment
from constants import ZERO_ADDRESS

class EVMMemFlowTest(unittest.TestCase):

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

    def testPop(self):
        code = '6011602250'
        environment = ExecutionEnvironment(code)
        self.evm.executeCode(environment)
        self.assertEqual(self.evm.stack.pop(), 0x11)

    def testAddress(self):
        code = '30'
        environment = ExecutionEnvironment(code)
        self.evm.executeCode(environment)
        self.assertEqual(self.evm.stack.pop(), ZERO_ADDRESS)


    def runTest(self):
        methods = dir(self)
        for method in methods:
            if method[:4] == 'test':
                getattr(self, method)()


if __name__ == '__main__':
    unittest.main()
