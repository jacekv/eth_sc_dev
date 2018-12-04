#modulo = 0x10000000000000000000000000000000000000000000000000000000000000000
import constants


def add(a, b):
    """
    Adds to numbers and doesn't let it become greater then
    2**256.

    Args:
        a: First value to which to second parameter is added
        b: Second value which is added to the first parameter
    """
    return (a + b) % constants.UINT256VALUE

def mul(a, b):
    """
    Multiplies to numbers and doesn't let it become greater then 2**256.

    Args:
        a: First value with which to second parameter is multiplied
        b: Second value which is multiplied with the first parameter
    """
    return (a * b) % constants.UINT256VALUE

def sub(a, b):
    """
    Subtracts two numbers and doesn't let it become greater then 2**256.

    Args:
        a: First value from which to second parameter is subtracted from
        b: Second value which is subtracted from the first parameter
    """
    return (a - b) % constants.UINT256VALUE

def power(a, b):
    """
    Calculates a raised to the power of b mod 2**256.

    Args:
        a: The base of the operation
        b: The exponent of the operation
    """
    return (a ** b) % constants.UINT256VALUE

def signextend(a, b):
    """
    Extends a signed number.

    Args:
        a: The size of the current value in bytes
        b: The value to be extended
    """
    if a <= 31:
        testbit = a * 8 + 7
        signBit = (1 << testbit)
        if b & signBit:
            return (b | (2**256 - signBit))
        else:
            return (b & (signBit - 1))
    else:
        return b
