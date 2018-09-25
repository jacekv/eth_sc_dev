import rlp
from sha3 import keccak_256

def calc_contract_address(sender, nonce):
    sender = bytes.fromhex(sender)
    return keccak_256(rlp.encode([sender, nonce])).hexdigest()[-40:]
