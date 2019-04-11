import unittest
import sys
import logging
import inspect

sys.path.append("../eth/")

from evm import EVM
from evm import State
from executionEnvironment import ExecutionEnvironment

class EVMDupTest(unittest.TestCase):

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

    def testDup1(self):
        code = '603380'
        self.execCode(code, 0x33)
        self.assertEqual(self.evm.stack.pop(), 0x33)

    def testDup2(self):
        code = '6011602281'
        self.execCode(code, 0x11)
        self.__checkStackValues(2, 0x22, 0x11)

    def testDup3(self):
        code = '60116022603382'
        self.execCode(code, 0x11)
        self.__checkStackValues(3, 0x33, 0x11)

    def testDup4(self):
        code = '601160226033604483'
        self.execCode(code, 0x11)
        self.__checkStackValues(4, 0x44, 0x11)

    def testDup5(self):
        code = '6011602260336044605584'
        self.execCode(code, 0x11)
        self.__checkStackValues(5, 0x55, 0x11)

    def testDup6(self):
        code = '60116022603360446055606685'
        self.execCode(code, 0x11)
        self.__checkStackValues(6, 0x66, 0x11)

    def testDup7(self):
        code = '601160226033604460556066607786'
        self.execCode(code, 0x11)
        self.__checkStackValues(7, 0x77, 0x11)

    def testDup8(self):
        code = '6011602260336044605560666077608887'
        self.execCode(code, 0x11)
        self.__checkStackValues(8, 0x88, 0x11)

    def testDup9(self):
        code = '60116022603360446055606660776088609988'
        self.execCode(code, 0x11)
        self.__checkStackValues(9, 0x99, 0x11)

    def testDup10(self):
        code = '60116022603360446055606660776088609960AA89'
        self.execCode(code, 0x11)
        self.__checkStackValues(10, 0xAA, 0x11)

    def testDup11(self):
        code = '60116022603360446055606660776088609960AA60BB8A'
        self.execCode(code, 0x11)
        self.__checkStackValues(11, 0xBB, 0x11)

    def testDup12(self):
        code = '60116022603360446055606660776088609960AA60BB60CC8B'
        self.execCode(code, 0x11)
        self.__checkStackValues(12, 0xCC, 0x11)

    def testDup13(self):
        code = '60116022603360446055606660776088609960AA60BB60CC60DD8C'
        self.execCode(code, 0x11)
        self.__checkStackValues(13, 0xDD, 0x11)

    def testDup14(self):
        code = '60116022603360446055606660776088609960AA60BB60CC60DD60EE8D'
        self.execCode(code, 0x11)
        self.__checkStackValues(14, 0xEE, 0x11)

    def testDup15(self):
        code = '60116022603360446055606660776088609960AA60BB60CC60DD60EE60FF8E'
        self.execCode(code, 0x11)
        self.__checkStackValues(15, 0xFF, 0x11)

    def testDup16(self):
        code = '60116022603360446055606660776088609960AA60BB60CC60DD60EE60FF60FF8F'
        self.execCode(code, 0x11)
        self.assertEqual(self.evm.stack.pop(), 0xFF)
        self.__checkStackValues(15, 0xFF, 0x11)

    def execCode(self, code, assertValue):
        environment = ExecutionEnvironment(code)
        #self.evm.setCode(code)
        self.evm.executeCode(State(), environment)
        self.assertEqual(self.evm.stack.pop(), assertValue)


    def __checkStackValues(self, depth, value, decrement):
        for i in range(0, depth):
            self.assertEqual(self.evm.stack.pop(), value)
            value -= decrement


    def runTest(self):
        methods = dir(self)
        for method in methods:
            if method[:4] == 'test':
                getattr(self, method)()


if __name__ == '__main__':
    unittest.main()
