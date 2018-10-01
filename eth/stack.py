from CallStackExceptions import *

class Stack(object):
    limit = 1024
    bitWidth = 256

    def __init__(self):
        self.stack = []
        self.size = 0
        
    def push(self, obj):
        """
        The functions pushes a value to the stack.

        Args
            obj (int): The value to be added to the stack.
        """
        if type(obj) != int:
            raise ValueError('Value is not a number.')
        if self.size >= 1024:
            raise CallStackDepthReached('Call stack depth has been reached.')
        if obj >= 2**self.bitWidth:
            raise CallStackValueToLarge('Value is to large for the stack.')
        #expand value to 256 bits
        entry = '{:064x}'.format(obj & (2**self.bitWidth - 1))
        self.stack.append(entry)
        self.size += 1

    def pop(self):
        """
        The function takes the latest value from the stack and returns it.

        Returns:
            int: The value which has been added the last.
        """
        self.size -= 1
        return self.stack.pop()

    def getStack(self):
        """
        Returns the whole stack.

        Returns:
            array: The while stack
        """
        return self.stack

s = Stack()
s.push(0xabcdef)
s.push(0x0213192038018098adadada5)
s.push(0x06)
#s.pop()
print(s.getStack())
