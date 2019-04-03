from sha3 import keccak_256

def keccak256(value):
    return keccak_256(bytearray.fromhex(value)).hexdigest()
