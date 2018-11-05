from memory import Memory
from stack import Stack
from storage import Storage
import re
import logging

class EVM(object):

    def __init__(self, code=""):
        """
        The function takes a solidity opcode string and executes each
        instruction one by one.
        """
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
        print(self.code)

    def __splitCode(self, code):
        codeSplitted = []
        pos = 0
        while pos < len(code):
            inst = int(code[pos:pos+2], 16)
            #here are the push codes
            if inst >= 0x60 and inst <= 0x7F:
                length = (inst - 0x60 + 1) * 2
                codeSplitted.push(code[pos:poslength])

        return codeSplitted

    def executeCode(self):
        """
        The function executes the opcode one by one.
        """
        while self.programCounter < len(self.code):
            opcode = self.code[self.programCounter]
            self.programCounter += 1
            if opcode[:3] == 'ADD':
                #we have a ADD opcode
                self.add()
            if opcode[:3] == 'SUB':
                #we have a ADD opcode
                self.sub()
            elif opcode[:4] == 'PUSH':
                #we have a push opcode, sp we push the next value
                self.push(int(opcode[4:]) * 2, self.code[self.programCounter])
                self.programCounter += 1
            elif opcode[:3] == 'DUP':
                #we have a duplicate, so we duplicate  a value from the stack
                self.dup(int(opcode[3:]))

    def push(self, size, data):
        """
        The function takes a value and adds it to the stack.

        Args:
            data: Value to be added to stack
        """
        if (len(data[2:]) > size):
            print("ERROR")
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

    def add(self):
        """
        Adds the top 2 values on the stack and pushes the result back onto
        the stack.
        """
        w1 = self.stack.pop()
        w2 = self.stack.pop()
        w3 = int(w1.getWord(), 16) + int(w2.getWord(), 16)
        self.stack.push(w3)

    def sub(self):
        """
        Subtracts the top 2 values on the stack from each other and pushes the
        result back onto the stack.
        """
        w1 = self.stack.pop()
        w2 = self.stack.pop()
        w3 = int(w1.getWord(), 16) - int(w2.getWord(), 16)
        self.stack.push(w3)

if __name__ == "__main__":
    #code = 'PUSH1 0x80 PUSH1 0x40 MSTORE CALLVALUE DUP1 ISZERO PUSH1 0xF JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH1 0x8E DUP1 PUSH2 0x1E PUSH1 0x0 CODECOPY PUSH1 0x0 RETURN STOP PUSH1 0x80 PUSH1 0x40 MSTORE PUSH1 0x4 CALLDATASIZE LT PUSH1 0x3F JUMPI PUSH1 0x0 CALLDATALOAD PUSH29 0x100000000000000000000000000000000000000000000000000000000 SWAP1 DIV PUSH4 0xFFFFFFFF AND DUP1 PUSH4 0xF8A8FD6D EQ PUSH1 0x44 JUMPI JUMPDEST PUSH1 0x0 DUP1 REVERT JUMPDEST CALLVALUE DUP1 ISZERO PUSH1 0x4F JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH1 0x56 PUSH1 0x58 JUMP JUMPDEST STOP JUMPDEST PUSH1 0x2 PUSH1 0x0 DUP2 SWAP1 SSTORE POP JUMP STOP LOG1 PUSH6 0x627A7A723058 KECCAK256 0xbb PUSH12 0x4D348508D72D3271A8A5EA59 0xb6 DUP6 PUSH22 0x3AEDBDB8A82E100AE8BD71A9A16AFA00290000000000'
    code = 'PUSH1 0x80 PUSH1 0x33 ADD'
    e = EVM(code)
    e.executeCode()
