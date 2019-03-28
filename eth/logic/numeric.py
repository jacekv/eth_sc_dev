import constants

def unsigedToSigned(value):
    """
    Converts a unsigned value to a signed value

    Args:
        value: An unsigned value

    Returns:
        Signed value
    """
    #check if the bit at position 255 is set
    if value > 0 and value & constants.UINT255VALUE == constants.UINT255VALUE:
        #if yes, the sign bit is set
        return (constants.UINT256VALUE - value) * - 1
    return value

def signedToUnsigned(value):
    """
    Converts a signed value to a unsigned value

    Args:
        value: A signed value

    Returns:
        Unsigned value
    """
    if value < 0:
        return constants.UINT256VALUE + value
    return value
