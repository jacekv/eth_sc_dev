from memory import Memory
from stack import Stack
from storage import Storage
import re
import logging

class Executor(object):

    def __init__(self, code):
        """
        The function takes a solidity opcode string and executes each
        instruction one by one.
        """
        self.code = code.split(' ')
        self.programCounter = 0
        self.stack = Stack()
        self.memory = Memory()
        logging.basicConfig(level=logging.INFO)
        logging.info('Initialized executor')

    def executeCode(self):
        """
        The function executes the opcode one by one.
        """
        while self.programCounter < len(self.code):
            opcode = self.code[self.programCounter]
            self.programCounter += 1
            logging.info('Executing opcode ' + opcode)
            if opcode[:4] == 'PUSH':
                #we have a push opcode, sp we push the next value
                self.push(self.code[self.programCounter])
                self.programCounter += 1
            elif opcode[:3] == 'DUP':
                #we have a duplicate, so we duplicate  a value from the stack
                self.dup(int(opcode[3:]))

    def push(self, data):
        """
        The function takes a value and adds it to the stack.

        Args:
            data: Value to be added to stack
        """
        logging.info('Pushing value {:s} to stack'.format(data))
        self.stack.push(int(data, 16))

    def dup(self, value):
        """
        Duplicates a value from the stack.

        Args:
            value: The valueth stack to be duplicated
        """
        if value < 1 or value > 16:
            logging.error('Invalid opcode')
        self.stack.push(value)


if __name__ == "__main__":
    code = 'PUSH1 0x80 PUSH1 0x40 MSTORE CALLVALUE DUP1 ISZERO PUSH1 0xF JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH1 0x8E DUP1 PUSH2 0x1E PUSH1 0x0 CODECOPY PUSH1 0x0 RETURN STOP PUSH1 0x80 PUSH1 0x40 MSTORE PUSH1 0x4 CALLDATASIZE LT PUSH1 0x3F JUMPI PUSH1 0x0 CALLDATALOAD PUSH29 0x100000000000000000000000000000000000000000000000000000000 SWAP1 DIV PUSH4 0xFFFFFFFF AND DUP1 PUSH4 0xF8A8FD6D EQ PUSH1 0x44 JUMPI JUMPDEST PUSH1 0x0 DUP1 REVERT JUMPDEST CALLVALUE DUP1 ISZERO PUSH1 0x4F JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH1 0x56 PUSH1 0x58 JUMP JUMPDEST STOP JUMPDEST PUSH1 0x2 PUSH1 0x0 DUP2 SWAP1 SSTORE POP JUMP STOP LOG1 PUSH6 0x627A7A723058 KECCAK256 0xbb PUSH12 0x4D348508D72D3271A8A5EA59 0xb6 DUP6 PUSH22 0x3AEDBDB8A82E100AE8BD71A9A16AFA00290000000000'

    e = Executor(code)
    e.executeCode()
