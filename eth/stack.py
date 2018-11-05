from CallStackExceptions import *
from word import Word

class Stack(object):
    limit = 1024

    def __init__(self, bitWidth=256):
        self.stack = []
        self.depth = 0
        if (bitWidth % 8 != 0):
            raise StackSizeInvalid('Stack word size not a multiple of 8')
        self.bitWidth = bitWidth

    def push(self, obj):
        """
        The functions pushes a value to the stack.

        Args
            obj (int): The value to be added to the stack.
        """
        if type(obj) != int:
            raise ValueError('Value is not a number.')
        if self.depth >= 1024:
            raise CallStackDepthReached('Call stack depth has been reached.')
        if obj >= 2**self.bitWidth:
            raise CallStackValueToLarge('Value is to large for the stack.')
        #expand value to 256 bits
        if self.bitWidth == 256:
            entry = Word(obj)
        else:
            entry = ('{:0' + str(int(self.bitWidth / 4)) + 'x}').format(obj)
        self.stack.append(entry)
        self.depth += 1

    def pop(self):
        """
        The function takes the latest value from the stack and returns it.

        Returns:
            int/word: Depending on the bit width of the stack, it returns int
                or word
        """
        self.depth -= 1
        return self.stack.pop()

    def getStack(self):
        """
        Returns the whole stack.

        Returns:
            array: The whole stack
        """
        return self.stack

    def getDepth(self):
        """
        Returns the stack depth

        Returns:
            int: The stack depth
        """
        return self.depth

    def dup(self, value):
        """
        Duplicates the valueth stack.

        Args:
            value: Valueth value to be duplicated
        """
        loc = self.depth - value
        v = self.stack[loc].getWord()
        self.push(v)
