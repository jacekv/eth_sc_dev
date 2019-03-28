import sys
sys.path.append((sys.path[0] + '/../'))
import time
from eth_typing import (
    Address,
    Hash32
)
from constants import (
    BLANK_ROOT_HASH,
    EMPTY_UNCLE_HASH,
    GENESIS_NONCE,
    ZERO_ADDRESS,
    ZERO_HASH32
)


class Blockheader:

    def __init__(self,
                 difficulty: int,
                 block_number: int,
                 gas_limit: int,
                 timestamp: int = None,
                 coinbase: Address = ZERO_ADDRESS,
                 parent_hash: Hash32 = ZERO_HASH32,
                 uncles_hash: Hash32 = EMPTY_UNCLE_HASH,
                 state_root: Hash32 = BLANK_ROOT_HASH,
                 transaction_root: Hash32 = BLANK_ROOT_HASH,
                 receipt_root: Hash32 = BLANK_ROOT_HASH,
                 bloom: int = 0,
                 gas_used: int = 0,
                 extra_data: bytes = b'',
                 mix_hash: Hash32 = ZERO_HASH32,
                 nonce: bytes = GENESIS_NONCE) -> None:
        if timestamp is None:
            timestamp = int(time.time())
        self.parent_hash = parent_hash
        self.uncles_hash = uncles_hash
        self.coinbase = coinbase
        self.state_root = state_root
        self.transaction_root = transaction_root
        self.receipt_root = receipt_root
        self.bloom = bloom
        self.difficulty = difficulty
        self.block_number = block_number
        self.gas_limit = gas_limit
        self.gas_used = gas_used
        self.timestamp = timestamp
        self.extra_data = extra_data
        self.mix_hash = mix_hash
        self.nonce = nonce
