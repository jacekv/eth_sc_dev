from math import ceil
from word import Word

"""
This is my implementation of the evm memory.

The memory is a volatile read-write byte-addressable space. It is mainly used
to store data during execution, mostly for passing arguments to internal
functions. Given this is volatile area, every message call starts with a
cleared memory. All locations are initially defined as zero. As calldata,
 memory can be addressed at byte level, but can only read 32-byte words
 at a time.

Memory is expanding when we write to to a word in it that was not previously
used. Additionally to the cost of the write itself, there is a cost to this
expansion, which increases linearly for the first 724 bytes and quadratically
after that.

The EVM provides three opcodes to interact with the memory area:

    MLOAD loads a word from memory into the stack.
    MSTORE saves a word to memory.
    MSTORE8 saves a byte to memory.

There is another key thing we need to know about memory. Solidity always stores
a free memory pointer at position 0x40, i.e. a reference to the first unused
word in memory. That’s why we load this word to operate with inline assembly.
Since the initial 64 bytes of memory are reserved for the EVM, this is how we
can ensure that we are not overwriting memory that is used internally by
Solidity.
"""


class Memory(object):

    def __init__(self):
        self.memory = []
        self.size = 0

    def mstore(self, address, data):
        """
        The function receives some data and stores it in the memory at the given
        address. It also checks if it needs to expand the memory.

        \param address (int) : Address where to store the data.
        \param data (int/str): The value to be stored in the memory.
        """
        word = Word(data)
        # location in array
        rest = int(address / 0x20)
        # location within word
        position = address % 0x20
        # we are not off
        if position == 0:
            self.memory[rest - 1] = word
        else:
            (high, low) = word.split(position - 1)
            self.memory[rest] = high
            self.memory[rest + 1] = low

    def mstore8(self, address, data):
        """
        Stores a single byte in the memory at the given address.

        \param address (int) : Address where to store the data.
        \param data (int/str): The value to be stored in the memory.

        """
        # location in array
        rest = int(address / 0x20)
        # location within word
        position = address % 0x20
        word = self.memory[rest]
        word.setByte(data, 31 - position)

    def expandMemory(self, address):
        """
        Function to expand the memory.

        \param address (int): The address where data is stored. Used to
            determine how much memory needs to be expanded
        """
        rest = ceil(address / 0x20)
        if ((address % 20) > 0):
            rest += 1
        for i in range(0, rest):
            self.memory.append(Word())
        self.size = len(self.memory)

    def getMemory(self):
        """
        Returns the whole memory content.

        \returns Array: Array containing Word objects.
        """
        return self.memory

    def getMemorySize(self):
        """
        Returns the size of the memory.

        \returns Int: The size of the memory.
        """
        return self.size

    def __str__(self):
        """
        Generated an output of the memory and returns it.

        \returns String: The memory representation.
        """
        output = ''
        address = 0
        for word in self.memory:
            output += '{:02x} - {:02x}: {:}\n'.format((address + 0x1F), address, word)
            address += 0x20
        return output
