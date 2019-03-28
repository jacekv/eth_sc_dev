import unittest
import sys
sys.path.append("../eth/")
import logging
import inspect

from evm import EVM
from executionEnvironment import ExecutionEnvironment
from constants import ZERO_ADDRESS


class EVMEnvInfoTest(unittest.TestCase):

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

    def testAddress(self):
        code = '30'
        environment = ExecutionEnvironment(code)
        self.evm.executeCode(environment)
        self.assertEqual(self.evm.stack.pop(), ZERO_ADDRESS)

    def testAddressNonZero(self):
        code = '30'
        environment = ExecutionEnvironment(code, addressOwningCode=0xea674fdde714fd979de3edf0f56aa9716b898ec8)
        self.evm.executeCode(environment)
        self.assertEqual(self.evm.stack.pop(), 0xea674fdde714fd979de3edf0f56aa9716b898ec8)

    def testOrigin(self):
        code = '32'
        environment = ExecutionEnvironment(code)
        self.evm.executeCode(environment)
        self.assertEqual(self.evm.stack.pop(), ZERO_ADDRESS)

    def testOriginNonZero(self):
        code = '32'
        environment = ExecutionEnvironment(code, senderAddress=0xea674fdde714fd979de3edf0f56aa9716b898ec8)
        self.evm.executeCode(environment)
        self.assertEqual(self.evm.stack.pop(), 0xea674fdde714fd979de3edf0f56aa9716b898ec8)

    def testCaller(self):
        code = '33'
        environment = ExecutionEnvironment(code)
        self.evm.executeCode(environment)
        self.assertEqual(self.evm.stack.pop(), ZERO_ADDRESS)

    def testCallerNonZero(self):
        code = '33'
        environment = ExecutionEnvironment(code, addressCausingExec=0xea674fdde714fd979de3edf0f56aa9716b898ec8)
        self.evm.executeCode(environment)
        self.assertEqual(self.evm.stack.pop(), 0xea674fdde714fd979de3edf0f56aa9716b898ec8)

    def testCallValue(self):
        code = '34'
        environment = ExecutionEnvironment(code)
        self.evm.executeCode(environment)
        self.assertEqual(self.evm.stack.pop(), 0)

    def testCallValueNonZero(self):
        code = '34'
        environment = ExecutionEnvironment(code, value=182736123)
        self.evm.executeCode(environment)
        self.assertEqual(self.evm.stack.pop(), 182736123)

    def testCallDataLoad(self):
        code = '600035'
        environment = ExecutionEnvironment(code)
        self.evm.executeCode(environment)
        self.assertEqual(self.evm.stack.pop(), 0)

    def testCallDataLoadNonZero(self):
        code = '600035602035'
        environment = ExecutionEnvironment(code, inputData='00000000000000000000000000000000000000000000000000000000b0f5aa210000000000000000000000000000000000000000000000000000000000000002')
        self.evm.executeCode(environment)
        print(self.evm.stack.getStack()[0])
        print(self.evm.stack.getStack()[1])
        self.assertEqual(self.evm.stack.pop(), 0x0000000000000000000000000000000000000000000000000000000000000002)
        self.assertEqual(self.evm.stack.pop(), 0x00000000000000000000000000000000000000000000000000000000b0f5aa21)

    def testCallDataSize(self):
        code = '36'
        environment = ExecutionEnvironment(code)
        self.evm.executeCode(environment)
        self.assertEqual(self.evm.stack.pop(), 0)

    def testCallDataSizeNonZero(self):
        code = '36'
        environment = ExecutionEnvironment(code, inputData='b0f5aa210000000000000000000000000000000000000000000000000000000000000002')
        self.evm.executeCode(environment)
        self.assertEqual(self.evm.stack.pop(), 36)

    def runTest(self):
        methods = dir(self)
        for method in methods:
            if method[:4] == 'test':
                getattr(self, method)()


if __name__ == '__main__':
    unittest.main()
