import unittest
import sys
sys.path.append("../eth/")
from evm import EVM

class CodeExeTest(unittest.TestCase):

    def setUp(self):
        self.evm = EVM()

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

if __name__ == '__main__':
    unittest.main()
