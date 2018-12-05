import constants

def equal(a, b):
    """
    Compares two signed values and checks wheather the values are equal

    Args:
        a: Left value
        b: Right value

    Returns:
        The result of a == b
    """
    return 1 if a == b else 0

def greater(a, b):
    """
    Compares two values and checks wheather the left value is greater

    Args:
        a: Left value
        b: Right value

    Returns:
        The result of a > b
    """
    return 1 if a > b else 0

def lesser(a, b):
    """
    Compares two values and checks wheather the left value is lesser

    Args:
        a: Left value
        b: Right value

    Returns:
        The result of a < b
    """
    return 1 if a < b else 0

def signedGreater(a, b):
    """
    Compares two signed values and checks wheather the left value is greater

    Args:
        a: Left value
        b: Right value

    Returns:
        The result of a > b
    """
    return 1 if __twoComplement(a) > __twoComplement(b) else 0

def signedLesser(a, b):
    """
    Compares two signed values and checks wheather the left value is lesser

    Args:
        a: Left value
        b: Right value

    Returns:
        The result of a < b
    """
    return 1 if __twoComplement(a) < __twoComplement(b) else 0

def isZero(a):
    """
    Checks if the given value is zero.

    Args:
        a: Value to be checked

    Returns:
        Result if value is zero
    """
    return 1 if a == 0 else 0

def bitwiseAnd(a, b):
    """
    Performs the bitwise AND operation

    Args:
        a: Left value
        b: Right value

    Returns:
        The result of a AND b
    """
    return a & b

def bitwiseOr(a, b):
    """
    Performs the bitwise OR operation

    Args:
        a: Left value
        b: Right value

    Returns:
        The result of a OR b
    """
    return a | b

def bitwiseXor(a, b):
    """
    Performs the bitwise XOR operation

    Args:
        a: Left value
        b: Right value

    Returns:
        The result of a XOR b
    """
    return a ^ b

def bitwiseNot(a):
    """
    Takes a value and performs the bitwise NOT operation.

    Args:
        a: Value

    Returns:
        Result of bitwise NOT operation
    """
    #We don't use pythons ~ bc it is for signed integers and we receive
    #a wrong result
    return constants.WORDMAXVALUE - a

def byte(a, b):
    """
    Takes a single byte from a byte32 value.

    Args:
        a: The position of the byte
        b: Byte32 value from where the byte is taken from

    Returns:
        Single byte from a byte32 value
    """
    b = '{0:064X}'.format(b)
    return int(b[a * 2: (a + 1) * 2], 16) if a < 32 else 0

def __twoComplement(value):
    """
    Switches between the number representation for negative numbers.

    Args:
        value: An integer, which representation might need to be changed

    Returns:
        Integer, where the representation might have changed (if needed)
    """
    #check if the bit at position 255 is set
    if value & 2**255 == 2**255 and value > 0:
        #if yes, the sign bit is set
        return (2**256 - value) * - 1
    #in case we have a negative value, we make the 2 complement of it
    if value < 0:
        return 2**256 + value
    return value
