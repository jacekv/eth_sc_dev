import unittest
import sys
sys.path.append("../eth/")
from evm import EVM
import logging

class EVMPushTest(unittest.TestCase):

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

    def testPush1(self):
        #push1 0x33
        code = '6033'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x33)

    def testPush2(self):
        code = '611122'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x1122)

    def testPush3(self):
        code = '62112233'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233)

    def testPush4(self):
        code = '6311223344'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x11223344)

    def testPush5(self):
        code = '641122334455'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x1122334455)

    def testPush6(self):
        code = '65112233445566'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566)

    def testPush7(self):
        code = '6611223344556677'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x11223344556677)

    def testPush8(self):
        code = '671122334455667788'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x1122334455667788)

    def testPush9(self):
        code = '68112233445566778899'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566778899)

    def testPush10(self):
        code = '69112233445566778899AA'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566778899AA)

    def testPush11(self):
        code = '6A112233445566778899AABB'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566778899AABB)

    def testPush12(self):
        code = '6B112233445566778899AABBCC'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566778899AABBCC)

    def testPush13(self):
        code = '6C112233445566778899AABBCCDD'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566778899AABBCCDD)

    def testPush14(self):
        code = '6D112233445566778899AABBCCDDEE'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566778899AABBCCDDEE)

    def testPush15(self):
        code = '6E112233445566778899AABBCCDDEEFF'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566778899AABBCCDDEEFF)

    def testPush16(self):
        code = '6F112233445566778899AABBCCDDEEFF00'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566778899AABBCCDDEEFF00)

    def testPush17(self):
        code = '70112233445566778899AABBCCDDEEFF0011'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566778899AABBCCDDEEFF0011)

    def testPush18(self):
        code = '71112233445566778899AABBCCDDEEFF001122'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566778899AABBCCDDEEFF001122)

    def testPush19(self):
        code = '72112233445566778899AABBCCDDEEFF00112233'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566778899AABBCCDDEEFF00112233)

    def testPush20(self):
        code = '73112233445566778899AABBCCDDEEFF0011223344'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566778899AABBCCDDEEFF0011223344)

    def testPush21(self):
        code = '74112233445566778899AABBCCDDEEFF001122334455'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566778899AABBCCDDEEFF001122334455)

    def testPush22(self):
        code = '75112233445566778899AABBCCDDEEFF00112233445566'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566778899AABBCCDDEEFF00112233445566)

    def testPush23(self):
        code = '76112233445566778899AABBCCDDEEFF0011223344556677'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566778899AABBCCDDEEFF0011223344556677)

    def testPush24(self):
        code = '77112233445566778899AABBCCDDEEFF001122334455667788'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566778899AABBCCDDEEFF001122334455667788)

    def testPush25(self):
        code = '78112233445566778899AABBCCDDEEFF00112233445566778899'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566778899AABBCCDDEEFF00112233445566778899)

    def testPush26(self):
        code = '79112233445566778899AABBCCDDEEFF00112233445566778899AA'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566778899AABBCCDDEEFF00112233445566778899AA)

    def testPush27(self):
        code = '7A112233445566778899AABBCCDDEEFF00112233445566778899AABB'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566778899AABBCCDDEEFF00112233445566778899AABB)

    def testPush28(self):
        code = '7B112233445566778899AABBCCDDEEFF00112233445566778899AABBCC'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566778899AABBCCDDEEFF00112233445566778899AABBCC)

    def testPush29(self):
        code = '7C112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDD'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDD)

    def testPush30(self):
        code = '7D112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDDEE'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDDEE)

    def testPush31(self):
        code = '7E112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDDEEFF'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDDEEFF)

    def testPush32(self):
        code = '7F112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDDEEFF00'
        self.evm.setCode(code)
        self.evm.executeCode()
        self.assertEqual(int(self.evm.stack.pop().getWord(), 16), 0x112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDDEEFF00)

    def runTest(self):
        methods = dir(self)
        for method in methods:
            if method[:4] == 'test':
                getattr(self, method)()
