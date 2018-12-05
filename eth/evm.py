from memory import Memory
from stack import Stack
from storage import Storage

import logic.arithmetic as arithmetic
import logic.bitwiseLogic as bitwiseLogic

import logging
import constants

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

            if inst >= 0x01 and inst <= 0x1A:
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
            if opcode >= 0x01 and opcode <= 0x0B:
                self.__simpleArithmetic(opcode)
            #elif opcode == 0x15:
            #    self.__isZero()
            elif opcode >= 0x10 and opcode <= 0x1A:
                self.__bitwiseOperations(opcode)
            elif opcode >= 0x60 and opcode <= 0x7F:
                #we have a push opcode, so we push the next value
                self.__push(self.code[self.programCounter][2:])
            elif opcode >= 0x80 and opcode <= 0x8F:
                #we have a duplicate, so we duplicate  a value from the stack
                self.__dup(opcode - 0x80)
            elif opcode >= 0x90 and opcode <= 0x9F:
                #SWAP opcode
                self.__swap(opcode - 0x90)
            self.programCounter += 1


    def __push(self, data):
        """
        The function takes a value and pushes it onto the stack.

        Args:
            data: Value to be added to stack
        """
        self.stack.push(int(data, 16))

    def __dup(self, value):
        """
        Duplicates a value from the stack.

        Args:
            value: The valueth stack to be duplicated
        """
        if value < 0 or value > 17:
            throw ('Invalid opcode')
        self.stack.dup(value + 1)

    def __swap(self, value):
        """
        Swapes the top most stack value with the stack value at given position
        value.

        Args:
            value: The valueth stack value to be swaped with the top most value
        """
        if value < 0 or value > 17:
            throw ('Invalid opcode')
        self.stack.swap(value + 1)

    def __simpleArithmetic(self, operation):
        """
        Performs simple arithmetic functions using two values from the stack.

        Args:
            operation: The arithmetic operation to perform
        """
        if operation == 0x01:
            #ADD
            s2 = arithmetic.add(*self.stack.pop(numItems=2))
        elif operation == 0x02:
            #MUL
            s2 = arithmetic.mul(*self.stack.pop(numItems=2))
        elif operation == 0x03:
            #SUB
            s2 = arithmetic.sub(*self.stack.pop(numItems=2))
        elif operation == 0x04:
            #DIV
            s2 = arithmetic.div(*self.stack.pop(numItems=2))
        elif operation == 0x05:
            #SDIV
            s2 = arithmetic.sdiv(*self.stack.pop(numItems=2))
            pass
        elif operation == 0x06:
            #MOD
            s2 = arithmetic.mod(*self.stack.pop(numItems=2))
        elif operation == 0x07:
            #SMOD
            s2 = arithmetic.smod(*self.stack.pop(numItems=2))
        elif operation == 0x08:
            #ADDMOD
            s2 = arithmetic.addmod(*self.stack.pop(numItems=3))
        elif operation == 0x09:
            #MULMOD
            s2 = arithmetic.mulmod(*self.stack.pop(numItems=3))
        elif operation == 0x0A:
            #EXP
            s2 = arithmetic.power(*self.stack.pop(numItems=2))
        elif operation == 0x0B:
            #SIGNEXTEND
            s2 = arithmetic.signextend(*self.stack.pop(numItems=2))
        self.stack.push(s2)


    def __bitwiseOperations(self, operation):
        """
        Contains different bitwise operations, such as AND, OR, XOR and NOT.

        Args:
            operation: Determines which bitwise function is executed
        """
        if operation == 0x10:
            #LT
            s2 = s2 = bitwiseLogic.lesser(*self.stack.pop(numItems=2))
        elif operation == 0x11:
            #GT
            s2 = bitwiseLogic.greater(*self.stack.pop(numItems=2))
        elif operation == 0x12:
            #SLT
            s2 = bitwiseLogic.signedLesser(*self.stack.pop(numItems=2))
        elif operation == 0x13:
            #SGT
            s2 = bitwiseLogic.signedGreater(*self.stack.pop(numItems=2))
        elif operation == 0x14:
            #EQ
            s2 = bitwiseLogic.equal(*self.stack.pop(numItems=2))
        elif operation == 0x15:
            #isZero
            s2 = bitwiseLogic.isZero(self.stack.pop())
        elif operation == 0x16:
            #AND
            s2 = bitwiseLogic.bitwiseAnd(*self.stack.pop(numItems=2))#s2 = s0 & s1
        elif operation == 0x17:
            #OR
            s2 = bitwiseLogic.bitwiseOr(*self.stack.pop(numItems=2))
        elif operation == 0x18:
            #XOR
            s2 = bitwiseLogic.bitwiseXor(*self.stack.pop(numItems=2))
        elif operation == 0x19:
            #NOT
            s2 = bitwiseLogic.bitwiseNot(self.stack.pop())
        elif operation == 0x1A:
            #BYTE
            s2 = bitwiseLogic.byte(*self.stack.pop(numItems=2))
        self.stack.push(s2)

#if __name__ == "__main__":
#    #code = 'PUSH1 0x80 PUSH1 0x40 MSTORE CALLVALUE DUP1 ISZERO PUSH1 0xF JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH1 0x8E DUP1 PUSH2 0x1E PUSH1 0x0 CODECOPY PUSH1 0x0 RETURN STOP PUSH1 0x80 PUSH1 0x40 MSTORE PUSH1 0x4 CALLDATASIZE LT PUSH1 0x3F JUMPI PUSH1 0x0 CALLDATALOAD PUSH29 0x100000000000000000000000000000000000000000000000000000000 SWAP1 DIV PUSH4 0xFFFFFFFF AND DUP1 PUSH4 0xF8A8FD6D EQ PUSH1 0x44 JUMPI JUMPDEST PUSH1 0x0 DUP1 REVERT JUMPDEST CALLVALUE DUP1 ISZERO PUSH1 0x4F JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH1 0x56 PUSH1 0x58 JUMP JUMPDEST STOP JUMPDEST PUSH1 0x2 PUSH1 0x0 DUP2 SWAP1 SSTORE POP JUMP STOP LOG1 PUSH6 0x627A7A723058 KECCAK256 0xbb PUSH12 0x4D348508D72D3271A8A5EA59 0xb6 DUP6 PUSH22 0x3AEDBDB8A82E100AE8BD71A9A16AFA00290000000000'
#    code = '7ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd606407'
#    e = EVM(code)
#    e.executeCode()
