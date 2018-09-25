import rlp
from sha3 import keccak_256

def calc_contract_address(sender, nonce):
    """
    The function takes the sender and the accounts nonce and calculates 
    the contracts address.

    \param sender (String): The address of the sender as a string.
    \param nonce (int): The hex representation of the sender's account nonce.

    \returns The contracts deployment address as string.
    """
    sender = bytes.fromhex(sender)
    return keccak_256(rlp.encode([sender, nonce])).hexdigest()[-40:]
