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
        self.execCode(code, 0x3377)

    def testAddOverflow(self):
        code = '7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff600201'
        self.execCode(code, 0x01)

    def testMultiplication(self):
        code = '603361334402'
        self.execCode(code, 0xA368C)

    def testSubstraction(self):
        code = '603361334403'
        self.execCode(code, 0x3311)

    def testDivisionNonZero(self):
        code = '603361334504'
        self.execCode(code, 0x101)

    def testSDivisionNonZero(self):
        code = '603361334505'
        self.execCode(code, 0x101)

    def testMod(self):
        code = '6022603306'
        self.execCode(code, 0x11)

    def testSMod1(self):
        code = '6003606407'
        self.execCode(code, 0x01)

    def testSMod2(self):
        #pushing -3 and 100 onto the stack
        code = '7Ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd606407'
        self.execCode(code, 0x01)

    def testSMod3(self):
        #pushing 3 and -100 onto the stack
        code = '60037Fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff9c07'
        self.execCode(code, 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)

    def testSMod4(self):
        #pushing -3 and -100 onto the stack
        code = '7Ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd7Fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff9c07'
        self.execCode(code, 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)

    def testAddmod(self):
        code = '60046007600308'
        self.execCode(code, 0x02)

    def testAddmod2(self):
        code = '61033F620181DB62BCCF0108'
        self.execCode(code, 0x3D)

    def testMulMod(self):
        code = '60036002600409'
        self.execCode(code, 0x02)

    def testExponentiation(self):
        code = '600260050A'
        self.execCode(code, 0x19)

    def testExponentiationOverflow(self):
        code = '60027F80000000000000000000000000000000000000000000000000000000000000000A'
        self.execCode(code, 0x00)

    def testSignextend(self):
        code = '60FE60000B'
        self.execCode(code, 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe)

    def testLtTrue(self):
        code = '603361334510'
        self.execCode(code, 0x0)

    def testLtFalse(self):
        code = '613345603310'
        self.execCode(code, 0x01)

    def testGtTrue(self):
        code = '603361334511'
        self.execCode(code, 0x01)

    def testGtFalse(self):
        code = '613345603311'
        self.execCode(code, 0x0)

    def testSltTrue1(self):
        code = '7Ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe7Ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd12'
        self.execCode(code, 0x01)

    def testSltTrue2(self):
        code = '60337Ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd12'
        self.execCode(code, 0x01)

    def testSltFalse1(self):
        code = '7Ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd7Ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe12'
        self.execCode(code, 0x0)

    def testSltFalse2(self):
        code = '7Ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd603312'
        self.execCode(code, 0x0)

    def testSgtTrue1(self):
        code = '7Ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd7Ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe13'
        self.execCode(code, 0x01)

    def testSgtTrue2(self):
        code = '7Ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd603313'
        self.execCode(code, 0x01)

    def testSgtFalse1(self):
        code = '7Ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe7Ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd13'
        self.execCode(code, 0x0)

    def testSgtFalse2(self):
        code = '60337Ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd13'
        self.execCode(code, 0x0)

    def testEqFalse(self):
        code = '613345603314'
        self.execCode(code, 0x0)

    def testEqTrue(self):
        code = '6033603314'
        self.execCode(code, 0x01)

    def execCode(self, code, assertValue):
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), assertValue)


    def runTest(self):
        methods = dir(self)
        for method in methods:
            if method[:4] == 'test':
                getattr(self, method)()


if __name__ == '__main__':
    unittest.main()
