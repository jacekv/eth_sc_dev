import constants

from utils.numeric import (
    unsigedToSigned,
    signedToUnsigned
)

def add(a, b):
    """
    Adds to numbers and doesn't let it become greater then
    2**256.

    Args:
        a: First value to which to second parameter is added
        b: Second value which is added to the first parameter

    Returns:
        Result of a + b
    """
    return (a + b) % constants.UINT256VALUE

def mul(a, b):
    """
    Multiplies to numbers and doesn't let it become greater then 2**256.

    Args:
        a: First value with which to second parameter is multiplied
        b: Second value which is multiplied with the first parameter

    Returns:
        Result of a * b
    """
    return (a * b) % constants.UINT256VALUE

def sub(a, b):
    """
    Subtracts two numbers and doesn't let it become greater then 2**256.

    Args:
        a: First value from which to second parameter is subtracted from
        b: Second value which is subtracted from the first parameter

    Returns:
        Result of a - b
    """
    return (a - b) % constants.UINT256VALUE

def div(a, b):
    """
    Calculates division

    Args:
        a: divident
        b: divisor

    Returns:
        Result of a / b
    """
    return 0 if b == 0 else int(a / b)

def sdiv(a, b):
    """
    Calculates signed division

    Args:
        a: divident
        b: divisor

    Returns:
        Result of a / b
    """
    a = unsigedToSigned(a)
    b = unsigedToSigned(b)
    return signedToUnsigned(div(a, b))

def mod(a, b):
    """
    Calculates the reminder

    Args:
        a: The divident
        b: The divisor

    Returns:
        The reminder of a divided by b
    """
    return 0 if b == 0 else a % b

def smod(a, b):
    """
    Calculates the reminder of two signed values

    Args:
        a: The divident
        b: The divisor

    Returns:
        The reminder of a divided by b
    """
    a = unsigedToSigned(a)
    b = unsigedToSigned(b)
    #based on this formula: (a/b)*b + a%b, we determine if the
    #reminder is negative or not
    return sub(a, mul(div(a, b), b))

def addmod(a, b, c):
    """
    Calculates add mod

    Args:
        a: Left add value
        b: Right add value
        c: Mod value

    Returns:
        Result of a * b mod c
    """
    return mod(add(a, b), c)

def mulmod(a, b, c):
    """
    Calculates mul mod

    Args:
        a: Left mul value
        b: Right mul value
        c: Mod value

    Returns:
        Result of a * b mod c
    """
    return mod(mul(a, b), c)

def power(a, b):
    """
    Calculates a raised to the power of b mod 2**256.

    Args:
        a: The base of the operation
        b: The exponent of the operation

    Returns:
        The result of a^b
    """
    return (a ** b) % constants.UINT256VALUE

def signextend(a, b):
    """
    Extends a signed number to 32 bytes.

    Args:
        a: The size of the current value in bytes
        b: The value to be extended

    Returns:
        Signextended number
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
