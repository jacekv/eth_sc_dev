from memory import Memory
from stack import Stack
from storage import Storage
import re
import logging

class EVM(object):

    def __init__(self, code="", logger=None):
        """
        The function takes a solidity opcode string and executes each
        instruction one by one.
        """
        self.logger = logger or logging.getLogger(__name__)
        if len(code) > 0:
            self.setCode(code)
        self.programCounter = 0
        self.stack = Stack()
        self.memory = Memory()


    def setCode(self, code):
        """
        Sets the code to be executed.
        """
        self.code = self.__splitCode(code)

    def __splitCode(self, code):
        codeSplitted = []
        pos = 0
        while pos < len(code):
            inst = int(code[pos:pos+2], 16)
            length = 2

            if inst >= 0x01 and inst <= 0x19:
                #add, sub, mul,... everything without a following paramter
                #but works directly with the stack
                codeSplitted.append(code[pos:pos+length])
            elif inst >= 0x60 and inst <= 0x7F:
                #PUSHX opcode
                length = (inst - 0x60 + 2) * 2
                codeSplitted.append(code[pos:pos+length])
            elif inst >= 0x80 and inst <= 0x9F:
                #dupX opcode
                codeSplitted.append(code[pos:pos+length])
            pos += length
        return codeSplitted

    def executeCode(self):
        """
        The function executes the opcode one by one.
        """
        self.programCounter = 0
        self.stack = Stack()
        self.memory = Memory()
        while self.programCounter < len(self.code):
            opcode = int(self.code[self.programCounter][:2], 16)
            if opcode == 0x00:
                #STOP instruction
                return
            if opcode >= 0x01 and opcode <= 0x14:
                self.simpleArithmetic(opcode)
            elif opcode == 0x15:
                self.isZero()
            elif opcode >= 0x16 and opcode <= 0x19:
                self.bitwiseOperations(opcode)
            elif opcode >= 0x60 and opcode <= 0x7F:
                #we have a push opcode, so we push the next value
                self.push(self.code[self.programCounter][2:])
            elif opcode >= 0x80 and opcode <= 0x8F:
                #we have a duplicate, so we duplicate  a value from the stack
                self.dup(opcode - 0x80)
            elif opcode >= 0x90 and opcode <= 0x9F:
                #SWAP opcode
                self.swap(opcode - 0x90)
            self.programCounter += 1


    def push(self, data):
        """
        The function takes a value and adds it to the stack.

        Args:
            data: Value to be added to stack
        """
        self.stack.push(int(data, 16))

    def dup(self, value):
        """
        Duplicates a value from the stack.

        Args:
            value: The valueth stack to be duplicated
        """
        if value < 0 or value > 17:
            throw ('Invalid opcode')
        self.stack.dup(value + 1)

    def swap(self, value):
        """
        """
        if value < 0 or value > 17:
            throw ('Invalid opcode')
        self.stack.swap(value + 1)

    def simpleArithmetic(self, operation):
        """
        Performs simple arithemtic functions using two values from the stack.

        Args:
            operation: The arithmetic operation to perform
        """
        v1 = int(self.stack.pop().getWord(), 16)
        v2 = int(self.stack.pop().getWord(), 16)
        if operation == 0x01:
            #ADD
            v3 = v1 + v2
        elif operation == 0x02:
            #MUL
            v3 = v1 * v2
        elif operation == 0x03:
            #SUB
            v3 = v1 - v2
        elif operation == 0x05:
            #DIV
            #we don't check if v2 is zero. Solidity should compile in such a way
            #that it checks :)
            v3 = int(v1 / v2)
        elif operation == 0x06:
            #MOD
            v3 = v1 % v2
        elif operation == 0x07:
            #SMOD
            v1 = self.__switchTwoComplement(v1)
            v2 = self.__switchTwoComplement(v2)
            #based on this formula, (a/b)*b + a%b, we determine if the
            #reminder is negative or not
            v3 = v1 - int(v1 / v2) * v2
            v3 = self.__switchTwoComplement(v3)
            #v3 = self.__switchTwoComplement(v3)
        elif operation == 0x10:
            #LT
            v3 = 1 if v1 < v2 else 0
        elif operation == 0x11:
            #GT
            v3 = 1 if v1 > v2 else 0
        elif operation == 0x12:
            #SLT
            v3 = 1 if self.__switchTwoComplement(v1) < self.__switchTwoComplement(v2) else 0
        elif operation == 0x13:
            #SGT
            v3 = 1 if self.__switchTwoComplement(v1) > self.__switchTwoComplement(v2) else 0
        elif operation == 0x14:
            #EQ
            v3 = 1 if v1 == v2 else 0
        self.stack.push(v3)

    def __switchTwoComplement(self, value):
        """
        Switches between the number representation for negative numbers.

        Args:
            value: An integer, which representation might need to be changed

        Returns:
            Integer, where the representation might have changed (if needed)
        """
        if value & 2**255 == 2**255 and value > 0:
            return (2**256 - value) * - 1
        if value < 0:
            return 2**256 + value
        return value

    def isZero(self):
        """
        Checks if the value on the stack is zero or not.
        """
        v1 = int(self.stack.pop().getWord(), 16)
        if v1 == 0:
            self.stack.push(1)
        else:
            self.stack.push(0)

    def bitwiseOperations(self, operation):
        """
        Contains different bitwise operations, such as AND, OR, XOR and NOT.

        Args:
            operation: Determines which bitwise function is executed
        """
        v1 = int(self.stack.pop().getWord(), 16)
        if operation != 0x19:
            v2 = int(self.stack.pop().getWord(), 16)
        if operation == 0x16:
            #AND
            v3 = v1 & v2
        elif operation == 0x17:
            #OR
            v3 = v1 | v2
        elif operation == 0x18:
            #XOR
            v3 = v1 ^ v2
        elif operation == 0x19:
            #NOT
            #We don't use pythons ~ bc it is for signed integers and we receive
            #a wrong result
            v3 = 2**256 - 1 - v1
        self.stack.push(v3)

if __name__ == "__main__":
    #code = 'PUSH1 0x80 PUSH1 0x40 MSTORE CALLVALUE DUP1 ISZERO PUSH1 0xF JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH1 0x8E DUP1 PUSH2 0x1E PUSH1 0x0 CODECOPY PUSH1 0x0 RETURN STOP PUSH1 0x80 PUSH1 0x40 MSTORE PUSH1 0x4 CALLDATASIZE LT PUSH1 0x3F JUMPI PUSH1 0x0 CALLDATALOAD PUSH29 0x100000000000000000000000000000000000000000000000000000000 SWAP1 DIV PUSH4 0xFFFFFFFF AND DUP1 PUSH4 0xF8A8FD6D EQ PUSH1 0x44 JUMPI JUMPDEST PUSH1 0x0 DUP1 REVERT JUMPDEST CALLVALUE DUP1 ISZERO PUSH1 0x4F JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH1 0x56 PUSH1 0x58 JUMP JUMPDEST STOP JUMPDEST PUSH1 0x2 PUSH1 0x0 DUP2 SWAP1 SSTORE POP JUMP STOP LOG1 PUSH6 0x627A7A723058 KECCAK256 0xbb PUSH12 0x4D348508D72D3271A8A5EA59 0xb6 DUP6 PUSH22 0x3AEDBDB8A82E100AE8BD71A9A16AFA00290000000000'
    code = '7ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd606407'
    e = EVM(code)
    e.executeCode()
