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

            if inst >= 0x01 and inst <= 0x14:
                #add, sub, mul,... everything without a following paramter
                #but works directly with the stack
                codeSplitted.append(code[pos:pos+length])
            elif inst >= 0x60 and inst <= 0x7F:
                #here are the push codes
                length = (inst - 0x60 + 2) * 2
                codeSplitted.append(code[pos:pos+length])
            elif inst >= 0x80 and inst <= 0x8F:
                #dupX opcode
                codeSplitted.append(code[pos:pos+length])
            pos += length
        return codeSplitted

    def executeCode(self):
        """
        The function executes the opcode one by one.
        """
        self.programCounter = 0
        while self.programCounter < len(self.code):
            opcode = int(self.code[self.programCounter][:2], 16)
            if opcode >= 0x01 and opcode <= 0x14:
                self.simpleArithmetic(opcode)
            elif opcode >= 0x60 and opcode <= 0x7F:
                #we have a push opcode, so we push the next value
                self.push(self.code[self.programCounter][2:])
            elif opcode >= 0x80 and opcode <= 0x8F:
                #we have a duplicate, so we duplicate  a value from the stack
                self.dup(opcode - 0x80)
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
        if value < 1 or value > 16:
            throw ('Invalid opcode')
        self.stack.push(value)

    def simpleArithmetic(self, operation):
        """
        Performs simole arithemtic functions using two values from the stack.

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
        elif operation == 0x10:
            #LT
            v3 = 1 if v1 < v2 else 0
        elif operation == 0x11:
            #GT
            v3 = 1 if v1 > v2 else 0
        elif operation == 0x14:
            #EQ
            v3 = 1 if v1 == v2 else 0
        self.stack.push(v3)


if __name__ == "__main__":
    #code = 'PUSH1 0x80 PUSH1 0x40 MSTORE CALLVALUE DUP1 ISZERO PUSH1 0xF JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH1 0x8E DUP1 PUSH2 0x1E PUSH1 0x0 CODECOPY PUSH1 0x0 RETURN STOP PUSH1 0x80 PUSH1 0x40 MSTORE PUSH1 0x4 CALLDATASIZE LT PUSH1 0x3F JUMPI PUSH1 0x0 CALLDATALOAD PUSH29 0x100000000000000000000000000000000000000000000000000000000 SWAP1 DIV PUSH4 0xFFFFFFFF AND DUP1 PUSH4 0xF8A8FD6D EQ PUSH1 0x44 JUMPI JUMPDEST PUSH1 0x0 DUP1 REVERT JUMPDEST CALLVALUE DUP1 ISZERO PUSH1 0x4F JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH1 0x56 PUSH1 0x58 JUMP JUMPDEST STOP JUMPDEST PUSH1 0x2 PUSH1 0x0 DUP2 SWAP1 SSTORE POP JUMP STOP LOG1 PUSH6 0x627A7A723058 KECCAK256 0xbb PUSH12 0x4D348508D72D3271A8A5EA59 0xb6 DUP6 PUSH22 0x3AEDBDB8A82E100AE8BD71A9A16AFA00290000000000'
    code = '603361334403'
    e = EVM(code)
    e.executeCode()
