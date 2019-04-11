import unittest
import sys
import logging
import inspect

sys.path.append("../eth/")
from evm import EVM
from evm import State
from executionEnvironment import ExecutionEnvironment

class EVMSwapTest(unittest.TestCase):

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

    def testSwap1(self):
        code = '6033601190'
        self.execCode(code, 0x33, 0x11)

    def testSwap2(self):
        code = '60116022603391'
        self.execCode(code, 0x11, 0x33)

    def testSwap3(self):
        code = '604460226033601192'
        self.execCode(code, 0x44, 0x11)

    def testSwap4(self):
        code = '6055602260336011603393'
        self.execCode(code, 0x55, 0x33)

    def testSwap5(self):
        code = '60556022603360116033603394'
        self.execCode(code, 0x55, 0x33)

    def testSwap6(self):
        code = '61553360226033601160336033604495'
        self.execCode(code, 0x5533, 0x44)

    def testSwap7(self):
        code = '615533602260336011603360336044603396'
        self.execCode(code, 0x5533, 0x33)

    def testSwap8(self):
        code = '61553360226033601160336033604460336233333397'
        self.execCode(code, 0x5533, 0x333333)

    def testSwap9(self):
        code = '62553344602260336011603360336044603362333333602298'
        self.execCode(code, 0x553344, 0x22)

    def testSwap10(self):
        code = '625533446022603360116033603360446033623333336022603399'
        self.execCode(code, 0x553344, 0x33)

    def testSwap11(self):
        code = '625533446022603360116033603360446033623333336022603360449A'
        self.execCode(code, 0x553344, 0x44)

    def testSwap12(self):
        code = '625533446022603360116033603360446033623333336022603360446133449B'
        self.execCode(code, 0x553344, 0x3344)

    def testSwap13(self):
        code = '6255334460226033601160336033604460336233333360226033604460336133449C'
        self.execCode(code, 0x553344, 0x3344)

    def testSwap14(self):
        code = '625533446022603360116033603360446033623333336022603360446033613344621122339D'
        self.execCode(code, 0x553344, 0x112233)

    def testSwap15(self):
        code = '6255334460226033601160336033604460336233333360226033604460336133446033621122339E'
        self.execCode(code, 0x553344, 0x112233)

    def testSwap16(self):
        code = '62553344602260336011603360336044603362333333602260336044603361334460336211223360AA9F'
        self.execCode(code, 0x553344, 0xAA)

    def execCode(self, code, assertValue, assertValue2):
        env = ExecutionEnvironment(code)
        self.evm.executeCode(State(), env)
        self.assertEqual(self.evm.stack.pop(), assertValue)
        self.assertEqual(int(self.evm.stack.getStack()[0].getWord(), 16), assertValue2)


    def runTest(self):
        methods = dir(self)
        for method in methods:
            if method[:4] == 'test':
                getattr(self, method)()


if __name__ == '__main__':
    unittest.main()
