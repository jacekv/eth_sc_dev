from memory import Memory
from stack import Stack
from storage import Storage

import logic.arithmetic as arithmetic
import logic.bitwiseLogic as bitwiseLogic
from math import ceil
from logic.sha3 import *

import logging
import constants


class EVM(object):

    def __init__(self, code="", logger=None):
        """
        The function takes a solidity opcode string and executes each
        instruction one by one.
        """
        self.logger = logger or logging.getLogger(__name__)
        self.programCounter: int
        self.code: list
        self.activeMemWords: int
        self.stack: Stack()
        self.memory: Memory

    def __splitCode(self, code) -> list:
        codeSplitted = []
        pos = 0
        while pos < len(code):
            inst = int(code[pos:pos + 2], 16)
            length = 2
            # We split the code in such a way, that parameters, which are within the code, are left together. As an
            # example: PUSH1. Push1 has one parameter and in the code it looks like this: 60FF. We push FF on the stack.
            # 61FFFF pushes 2 bytes on the stack. Since the FFFF is the parameter, we don't split it, but we leave it
            # together in the code: 61FFFF 'SPACE' 'Next opcode'.
            if inst >= 0x60 and inst <= 0x7F:
                # PUSHX opcode
                length = (inst - 0x60 + 2) * 2
                codeSplitted.append(code[pos:pos + length])
            else:
                # all the opcodes, which have no parameters
                codeSplitted.append(code[pos:pos + length])
            pos += length

        return codeSplitted

    def executeCode(self, environment) -> None:
        """
        The function executes the opcode one by one.
        """
        self.code = self.__splitCode(environment.machineCode)
        self.programCounter = 0
        # active word in memory mue_i in execution environment
        self.activeMemWords = 0
        self.stack = Stack()
        self.memory = Memory()
        while self.programCounter < len(self.code):
            opcode = int(self.code[self.programCounter][:2], 16)
            if opcode == 0x00:
                # STOP instruction
                return
            if opcode >= 0x01 and opcode <= 0x0B:
                self.__simpleArithmetic(opcode)
            elif opcode >= 0x10 and opcode <= 0x1A:
                self.__bitwiseOperations(opcode)
            elif opcode >= 0x30 and opcode <= 0x3E:
                self.__environmentalInfo(opcode, environment)
            elif opcode >= 0x40 and opcode <= 0x45:
                self.__blockInformation(opcode, environment)
            elif opcode >= 0x50 and opcode <= 0x5B:
                self.__memFlowOperations(opcode)
            elif opcode >= 0x60 and opcode <= 0x7F:
                # we have a push opcode, so we push the next value
                self.__push(self.code[self.programCounter][2:])
            elif opcode >= 0x80 and opcode <= 0x8F:
                # we have a duplicate, so we duplicate  a value from the stack
                self.__dup(opcode - 0x80)
            elif opcode >= 0x90 and opcode <= 0x9F:
                # SWAP opcode
                self.__swap(opcode - 0x90)
            self.programCounter += 1

    def __push(self, data) -> None:
        """
        The function takes a value and pushes it onto the stack.

        Args:
            data: Value to be added to stack
        """
        self.stack.push(int(data, 16))

    def __pop(self) -> None:
        """
        The function removes the top most entry from the stack.
        """
        self.stack.pop()

    def __dup(self, value) -> None:
        """
        Duplicates a value from the stack.

        Args:
            value: The valueth stack to be duplicated
        """
        if value < 0 or value > 17:
            throw('Invalid opcode')
        self.stack.dup(value + 1)

    def __swap(self, value) -> None:
        """
        Swapes the top most stack value with the stack value at given position
        value.

        Args:
            value: The valueth stack value to be swaped with the top most value
        """
        if value < 0 or value > 17:
            throw('Invalid opcode')
        self.stack.swap(value + 1)

    def __simpleArithmetic(self, operation) -> None:
        """
        Performs simple arithmetic functions using two values from the stack.

        Args:
            operation: The arithmetic operation to perform
        """
        if operation == 0x01:
            # ADD
            s2 = arithmetic.add(*self.stack.pop(numItems=2))
        elif operation == 0x02:
            # MUL
            s2 = arithmetic.mul(*self.stack.pop(numItems=2))
        elif operation == 0x03:
            # SUB
            s2 = arithmetic.sub(*self.stack.pop(numItems=2))
        elif operation == 0x04:
            # DIV
            s2 = arithmetic.div(*self.stack.pop(numItems=2))
        elif operation == 0x05:
            # SDIV
            s2 = arithmetic.sdiv(*self.stack.pop(numItems=2))
        elif operation == 0x06:
            # MOD
            s2 = arithmetic.mod(*self.stack.pop(numItems=2))
        elif operation == 0x07:
            # SMOD
            s2 = arithmetic.smod(*self.stack.pop(numItems=2))
        elif operation == 0x08:
            # ADDMOD
            s2 = arithmetic.addmod(*self.stack.pop(numItems=3))
        elif operation == 0x09:
            # MULMOD
            s2 = arithmetic.mulmod(*self.stack.pop(numItems=3))
        elif operation == 0x0A:
            # EXP
            s2 = arithmetic.power(*self.stack.pop(numItems=2))
        elif operation == 0x0B:
            # SIGNEXTEND
            s2 = arithmetic.signextend(*self.stack.pop(numItems=2))
        self.stack.push(s2)

    def __bitwiseOperations(self, operation) -> None:
        """
        Contains different bitwise operations, such as AND, OR, XOR and NOT.

        Args:
            operation: Determines which bitwise function is executed
        """
        if operation == 0x10:
            # LT
            s2 = s2 = bitwiseLogic.lesser(*self.stack.pop(numItems=2))
        elif operation == 0x11:
            # GT
            s2 = bitwiseLogic.greater(*self.stack.pop(numItems=2))
        elif operation == 0x12:
            # SLT
            s2 = bitwiseLogic.signedLesser(*self.stack.pop(numItems=2))
        elif operation == 0x13:
            # SGT
            s2 = bitwiseLogic.signedGreater(*self.stack.pop(numItems=2))
        elif operation == 0x14:
            # EQ
            s2 = bitwiseLogic.equal(*self.stack.pop(numItems=2))
        elif operation == 0x15:
            # isZero
            s2 = bitwiseLogic.isZero(self.stack.pop())
        elif operation == 0x16:
            # AND
            s2 = bitwiseLogic.bitwiseAnd(*self.stack.pop(numItems=2))  # s2 = s0 & s1
        elif operation == 0x17:
            # OR
            s2 = bitwiseLogic.bitwiseOr(*self.stack.pop(numItems=2))
        elif operation == 0x18:
            # XOR
            s2 = bitwiseLogic.bitwiseXor(*self.stack.pop(numItems=2))
        elif operation == 0x19:
            # NOT
            s2 = bitwiseLogic.bitwiseNot(self.stack.pop())
        elif operation == 0x1A:
            # BYTE
            s2 = bitwiseLogic.byte(*self.stack.pop(numItems=2))
        self.stack.push(s2)

    def __environmentalInfo(self, operation, environment) -> None:
        """
        Contains different environment operations, such as ADDRESS, BALANCE, ORIGIN, CALLER, CALLVALUE and more

        Args:
            operation: Determines which environment function is executed
            environment: The environment, which contains all necessary information
        """
        if operation == 0x30:
            # ADDRESS
            self.stack.push(environment.addressOwningCode)
        elif operation == 0x31:
            # BALANCE
            pass
        elif operation == 0x32:
            # ORIGIN
            self.stack.push(environment.senderAddress)
        elif operation == 0x33:
            # CALLER
            self.stack.push(environment.addressCausingExec)
        elif operation == 0x34:
            # CALLVALUE
            self.stack.push(environment.value)
        elif operation == 0x35:
            # CALDATALOAD
            start = self.stack.pop() * 2
            # 62 = 31 * 2 + 2, since we have bytes and each byte has 2 chars and 64 is excluded
            self.stack.push(int(environment.inputData[start: start + 64], 16))
        elif operation == 0x36:
            # CALLDATASIZE
            # divide by 2, since we have bytes
            self.stack.push(int(len(environment.inputData) / 2))
        elif operation == 0x37:
            # CALLDATACOPY
            sdata = self.stack.pop(numItems=3)
            callData = environment.inputData
            callDataLen = len(callData)
            start = sdata[1] * 2
            # mul 2 because it is a string of bytes
            for i in range(0, sdata[2] * 2, 2):
                if (start + i) < callDataLen:
                    d = int(callData[start + i: start + i + 2], 16)
                else:
                    d = 0
                # div 2 because it cals the steps for the mem location wrong, due to the 2 steps in the loop
                self.memory.mstore8(sdata[0] + int(i/2), d)
            self.activeMemWords = self.__mem_expansion(self.activeMemWords, sdata[0], sdata[2])
        elif operation == 0x38:
            # CODESIZE
            self.stack.push(int(len(environment.machineCode) / 2))
        elif operation == 0x39:
            # CODECOPY
            raise NotImplemented('CODECOPY')
        elif operation == 0x3A:
            # GASPRICE
            self.stack.push(environment.gasPrice)
        elif operation == 0x3B:
            # EXTCODESIZE
            raise NotImplemented('EXTCODESIZE')
        elif operation == 0x3C:
            # EXTCODECOPY
            raise NotImplemented('EXTCODECOPY')
        elif operation == 0x3D:
            # RETURNDATASIZE
            raise NotImplemented('RETURNDATASIZE')
        elif operation == 0x3E:
            # RETURNDATACOPY
            raise NotImplemented('RETURNDATACOPY')

    def __blockInformation(self, opcode, environment) -> None:
        """
        Contains different block information operations, BLOCKHASH, COINBASE, TIMESTAMP, NUMBER and more

        Args:
            operation: Determines which block information operation is executed
            environment: The environment, which contains all necessary information
        """
        if opcode == 0x40:
            # BLOCKHASH
            raise NotADirectoryError('BLOCKHASH')
        elif opcode == 0x41:
            # COINBASE
            self.stack.push(environment.blockHeader.coinbase)
        elif opcode == 0x42:
            # TIMESTAMP
            self.stack.push(environment.blockHeader.timestamp)
        elif opcode == 0x43:
            # NUMBER
            self.stack.push(environment.blockHeader.block_number)
        elif opcode == 0x44:
            # DIFFICULTY
            self.stack.push(environment.blockHeader.difficulty)
        elif opcode == 0x45:
            # GASLIMIT
            self.stack.push(environment.blockHeader.gas_limit)

    def __memFlowOperations(self, opcode) -> None:
        """
        Contains different memory and flow operations, such as JUMP, PC, MSIZE, GAS and more

        Args:
            operation: Determines which flow operation is executed
        """
        if opcode == 0x50:
            # POP
            self.stack.pop()
        elif opcode == 0x51:
            # MLOAD
            word = self.memory.mload(self.stack.pop()).getWord()
            self.stack.push(int(word, 16))
            self.activeMemWords = max(self.activeMemWords, self.memory.getMemorySize())
        elif opcode == 0x52:
            # MSTORE
            data = self.stack.pop(numItems=2)
            # expand if needed
            self.memory.expandMemory(data[0])
            self.memory.mstore(*data)
            mem = self.memory.getMemory()
            self.activeMemWords = max(self.activeMemWords, self.memory.getMemorySize())
        elif opcode == 0x53:
            # MSTORE8
            data = self.stack.pop(numItems=2)
            # expand if needed
            self.memory.expandMemory(data[0])
            self.memory.mstore8(*data)
            self.activeMemWords = max(self.activeMemWords, self.memory.getMemorySize())
        elif opcode == 0x54:
            # SLOAD
            raise NotImplemented('SLOAD')
        elif opcode == 0x55:
            # SSTORE
            raise NotImplemented('SSTORE')
        elif opcode == 0x56:
            # JUMP
            # -1 because PC is incremented afterwards
            self.programCounter = self.stack.pop() - 1
        elif opcode == 0x57:
            # JUMPI
            loc = self.stack.pop()
            cond = self.stack.pop()
            if cond != 0:
                self.programCounter = loc - 1
        elif opcode == 0x58:
            # PC
            self.stack.push(self.programCounter)
        elif opcode == 0x59:
            # MSIZE
            size = self.memory.getMemorySize()
            self.stack.push((self.activeMemWords * 32))
        elif opcode == 0x5A:
            # GAS
            raise NotImplemented('GAS')
        elif opcode == 0x5B:
            # JUMPDEST
            # not sure what is happening here
            pass


    def __mem_expansion(self, s: int, f:int, l: int) -> int:
        if l == 0:
            return s
        max(s, ceil((f+l) / 32))
