import string
from utils import *

class Word(object):
    def __init__(self, value=0, offset=0):
        """
        Constructor

        \param value (int) : The initial value for the word.
        \param offset (int): Offset for the byte in the word.
        """
        self.setWord(value, offset)

    def setWord(self, value, offset=0):
        """
        The function setWord is used to set a new value.

        \param value (int/str): The new value for the word.
        \param offset (int): Offset for the byte in the word.
        """
        if (type(value) != int and type(value) != str):
            raise ValueError('Value is not of type int or str.')
        if (type(value) == str):
            #check if we have a hex value given
            if (value[:2] == '0x'):
                #does it contain valid hex characters?
                if (utils.isHex(value[2:])):
                    #if yes, cast to int
                    value = int(value, 16)
                else:
                    #otherwise, you know
                    raise ValueError('Given value contains illegal characters.')
            else:
                #no hex value, so we go for base 10
                value = int(value)
        #does it have more than 32 bytes?
        if (value > 2**256):
            raise ValueError('Given value larger than 2**256.')
        if (offset > 31):
            raise ValueError('Offset larger than 32 bytes.')
        #format and set!
        self.value = '{:064x}'.format(value << (offset * 8))


    def getWord(self):
        """
        The function returns the value of the word.

        \returns String: Value of the word.
        """
        return self.value

    def setByte(self, value, position):
        """
        Sets a single byte at the given position in the memory.

        \param value (int/str): The value to be set.
        \param position (int) : The position in the word where the value should
            be set.
        """
        if (type(value) != int and type(value) != str):
            raise ValueError('Value is not of type int or str.')
        if (position > 31):
            raise ValueError("Position {} is out of word.".format(position))
        position *= 2
        if (type(value) == str):
            if (value[:2] == '0x'):
                #does it contain valid hex characters?
                if (utils.isHex(value[2:4])):
                    #if yes, cast to int
                    value = int(value, 16)
                else:
                    #otherwise, you know
                    raise ValueError('Given value contains illegal characters.')
            else:
                #no hex value, so we go for base 10
                value = int(value)
        self.value = self.value[:position] + '{:02x}'.format(value % 256) + self.value[position+2:]


    def getByte(self, byte):
        """
        The function returns a single byte at the given position of the word.

        \param byte (int): Position of byte to extract.

        \returns string: The single byte at the given position.
        """
        if (type(byte) != int):
            raise ValueError('Value is not of type int.')
        elif (byte > 32):
            raise ValueError('Value is larger than 32.')
        #bytes times 2, since we have 64 positions
        byte *= 2
        #reverse value and extract the byte
        return (self.value[::-1])[byte:byte+2]

    def getLsb(self):
        """
        Returns the least significant byte of the word.

        \returns string: The lsb of the word.
        """
        return self.getByte(0)

    def getMsb(self):
        """
        Returns the most significant byte of the word.

        \returns string: The msb of the word.
        """
        return self.getByte(31)

    def split(self, byte):
        """
        Splits the word at the given position, whereby the byte at which point
        it is splitted is added to the lower part. Both parts are padded by
        leading/following zeros.

        \returns tuple: Contains the high and the low part of the word.
        """
        byte = (31 - byte ) * 2
        low = Word('0x{:0<64}'.format(self.value[byte:]))
        high = Word('0x' + self.value[:byte])
        return (high, low)

    def __str__(self):
        return self.value
