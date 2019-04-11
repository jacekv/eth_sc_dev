from word import Word

class Storage(object):

    def __init__(self):
        self.storage = {}

    def sstore(self, key, data):
        """
        Function sstore stores data in storage at the given address.

        \param int      : The address on where to store the data
        \param (int/str): The data to be stored in the storage
        """
        if key >= 2**256:
            raise ValueError('Given key can\'t be larger than 2**256.')
        if type(key) != 'int':
            raise ValueError('Key is not of type int.')
        if key in self.storage:
            self.storage[key].setWord(data)
        else:
            self.storage[key] = Word(data)

    def sload(self, key):
        """
        The function returns the data located at the given address. In case
        there is no data stored, a zero-word is returned.

        \param int: The address the data to be retrieved from

        \returns String: The data stored at the given address.
        """
        if key in self.storage:
            return self.storage[key].getWord()
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
