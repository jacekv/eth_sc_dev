import unittest
import sys

sys.path.append("../eth/")
import logging
import time

from evm import EVM
from evm import State
from executionEnvironment import ExecutionEnvironment
from structures.blockHeader import Blockheader
from constants import ZERO_ADDRESS


class EVMBlockInfoTest(unittest.TestCase):

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

    def testCoinbase(self):
        code = '41'
        b = Blockheader(0, 0, 0, coinbase=ZERO_ADDRESS)
        environment = ExecutionEnvironment(code, blockHeader=b)
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), ZERO_ADDRESS)

    def testCoinbase2(self):
        code = '41'
        b = Blockheader(0, 0, 0, coinbase=0x5a0b54d5dc17e0aadc383d2db43b0a0d3e029c4c)
        environment = ExecutionEnvironment(code, blockHeader=b)
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), 0x5a0b54d5dc17e0aadc383d2db43b0a0d3e029c4c)

    def testTimestamp(self):
        code = '42'
        t = int(time.time())
        b = Blockheader(0, 0, 0, timestamp=t)
        environment = ExecutionEnvironment(code, blockHeader=b)
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), t)

    def testBlockNumber(self):
        code = '43'
        b = Blockheader(0, 1337, 0)
        environment = ExecutionEnvironment(code, blockHeader=b)
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), 1337)

    def testBlockDifficulty(self):
        code = '44'
        b = Blockheader(918237, 1337, 0)
        environment = ExecutionEnvironment(code, blockHeader=b)
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), 918237)

    def testBlockGasLimit(self):
        code = '45'
        b = Blockheader(918237, 1337, 12987319273)
        environment = ExecutionEnvironment(code, blockHeader=b)
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), 12987319273)

    def runTest(self):
        methods = dir(self)
        for method in methods:
            if method[:4] == 'test':
                getattr(self, method)()


if __name__ == '__main__':
    unittest.main()
