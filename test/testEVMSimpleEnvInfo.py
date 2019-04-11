import unittest
import sys
sys.path.append("../eth/")
import logging
import inspect

from evm import EVM
from state import State

from executionEnvironment import ExecutionEnvironment
from constants import ZERO_ADDRESS
from constants import Address


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
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), ZERO_ADDRESS)

    def testAddressNonZero(self):
        code = '30'
        environment = ExecutionEnvironment(code, addressOwningCode=0xea674fdde714fd979de3edf0f56aa9716b898ec8)
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), 0xea674fdde714fd979de3edf0f56aa9716b898ec8)

    def testBalance(self):
        code = '732a5994b501e6a560e727b6c2de5d856396aadd3831'
        environment = ExecutionEnvironment(code)
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), 0)

    def testBalanceNotZero(self):
        code = '732a5994b501e6a560e727b6c2de5d856396aadd3831'
        environment = ExecutionEnvironment(code)
        s = State()
        s.storage[0x2a5994b501e6a560e727b6c2de5d856396aadd38] = {'balance': 1337}
        self.evm.executeCode(s, environment)
        self.assertEqual(self.evm.stack.pop(), 1337)

    def testOrigin(self):
        code = '32'
        environment = ExecutionEnvironment(code)
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), ZERO_ADDRESS)

    def testOriginNonZero(self):
        code = '32'
        environment = ExecutionEnvironment(code, senderAddress=0xea674fdde714fd979de3edf0f56aa9716b898ec8)
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), 0xea674fdde714fd979de3edf0f56aa9716b898ec8)

    def testCaller(self):
        code = '33'
        environment = ExecutionEnvironment(code)
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), ZERO_ADDRESS)

    def testCallerNonZero(self):
        code = '33'
        environment = ExecutionEnvironment(code, addressCausingExec=0xea674fdde714fd979de3edf0f56aa9716b898ec8)
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), 0xea674fdde714fd979de3edf0f56aa9716b898ec8)

    def testCallValue(self):
        code = '34'
        environment = ExecutionEnvironment(code)
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), 0)

    def testCallValueNonZero(self):
        code = '34'
        environment = ExecutionEnvironment(code, value=182736123)
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), 182736123)

    def testCallDataLoad(self):
        code = '600035'
        environment = ExecutionEnvironment(code)
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), 0)

    def testCallDataLoadNonZero(self):
        code = '600035602035'
        environment = ExecutionEnvironment(code, inputData='00000000000000000000000000000000000000000000000000000000b0f5aa210000000000000000000000000000000000000000000000000000000000000002')
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), 0x0000000000000000000000000000000000000000000000000000000000000002)
        self.assertEqual(self.evm.stack.pop(), 0x00000000000000000000000000000000000000000000000000000000b0f5aa21)

    def testCallDataSize(self):
        code = '36'
        environment = ExecutionEnvironment(code)
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), 0)

    def testCallDataSizeNonZero(self):
        code = '36'
        environment = ExecutionEnvironment(code, inputData='b0f5aa210000000000000000000000000000000000000000000000000000000000000002')
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), 36)

    def testCallDataCopy(self):
        code = '60046002600037'
        environment = ExecutionEnvironment(code, inputData='11223344556677000000000000000000000000000000000000000000b0f5aa210000000000000000000000000000000000000000000000000000000000000002')
        self.evm.executeCode(State(), environment)
        mem = self.evm.memory.getMemory()
        self.assertEqual(mem[0].getWord(), '3344556600000000000000000000000000000000000000000000000000000000')

    def testCallDataCopy2(self):
        code = '601F6032600037'
        environment = ExecutionEnvironment(code, inputData='11223344556677000000000000000000000000000000000000000000b0f5aa21000000000000000000000000000000000000112233445566778899AABBCCDD02')
        self.evm.executeCode(State(), environment)
        mem = self.evm.memory.getMemory()
        self.assertEqual(mem[0].getWord(), '112233445566778899aabbccdd02000000000000000000000000000000000000')

    def testCodeCopy(self):
        code = '60076000600039'
        environment = ExecutionEnvironment(code)
        self.evm.executeCode(State(), environment)
        mem = self.evm.memory.getMemory()
        self.assertEqual(mem[0].getWord(), '6007600060003900000000000000000000000000000000000000000000000000')

    def testCodeCopy(self):
        code = '60086000600039'
        environment = ExecutionEnvironment(code)
        self.evm.executeCode(State(), environment)
        mem = self.evm.memory.getMemory()
        self.assertEqual(mem[0].getWord(), '6008600060003900000000000000000000000000000000000000000000000000')


    def testCodeSize(self):
        code = '38'
        environment = ExecutionEnvironment(code)
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), 1)

    def testCodeSize2(self):
        code = '600035602038'
        environment = ExecutionEnvironment(code)
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), 6)

    def testGasPrice(self):
        code = '3A'
        environment = ExecutionEnvironment(code)
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), 0)

    def testGasPriceNonZero(self):
        code = '3A'
        environment = ExecutionEnvironment(code, gasPrice=21000)
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), 21000)

    def runTest(self):
        methods = dir(self)
        for method in methods:
            if method[:4] == 'test':
                getattr(self, method)()


if __name__ == '__main__':
    unittest.main()
