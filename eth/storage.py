from word import Word

class Storage(object):

    def __init__(self):
        self.storage = {}

    def sstore(self, address, data):
        """
        Function sstore stores data in storage at the given address.

        \param int      : The address on where to store the data
        \param (int/str): The data to be stored in the storage
        """
        if address >= 2**256:
            raise ValueError('Given address can\'t be larger than 2**256.')
        if type(address) != 'int':
            raise ValueError('Address is not of type int.')
        if address in self.storage:
            self.storage[address].setWord(data)
        else:
            self.storage[address] = Word(data)

    def sload(self, address):
        """
        The function returns the data located at the given address. In case
        there is no data stored, a zero-word is returned.

        \param int: The address the data to be retrieved from

        \returns String: The data stored at the given address.
        """
        if address in self.storage:
            return self.storage[address].getWord()
        else:
            return '00' * 32

    def __str__(self):
        """
        The function __str__ creates a representation of the storage and
        returns it.

        \returns String: The storage
        """
        output = ''
        for k in self.storage:
            output += (hex(k) + '  ' + self.storage[k].getWord())
        return output

if __name__ == '__main__':
    s = Storage()
    s.sstore(0x40, 0xAABBDDCC)
    print(s)
