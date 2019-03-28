from sha3 import keccak_256

def keccak256(value):
    value = '{0:x}'.format(value)
    return keccak_256(bytearray.fromhex(value)).hexdigest()
