from CallStackExceptions import *

class Stack(object):
    limit = 1024
    bitWidth = 256

    def __init__(self):
        self.stack = []
        self.size = 0
        
    def push(self, obj):
        if self.size >= 1024:
            raise CallStackDepthReached('Call stack depth has been reached.')
        if(type(obj) == int):
            print('Adding int')
            entry = '{:064x}'.format(obj & (2**self.bitWidth - 1))
            self.stack.append(obj)

    def pop(self):
        return self.stack.pop()

    def getStack(self):
        return self.stack

s = Stack()
s.push(4)
s.push(5)
s.push(-6)
#s.pop()
print(s.getStack())
