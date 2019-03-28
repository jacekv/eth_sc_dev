from eth_typing import (
    Address,
    Hash32
)

UINT256 = 'uint256'
WORD = 'word'

UINT256VALUE = 2**256
UINT255VALUE = 2**255
WORDMAXVALUE = 2**256 - 1

ZERO_ADDRESS = Address(20 * b'\x00')
ZERO_HASH32 = Hash32(32 * b'\x00')

GENESIS_NONCE = b'\x00\x00\x00\x00\x00\x00\x00B'

EMPTY_UNCLE_HASH = Hash32(b'\x1d\xccM\xe8\xde\xc7]z\xab\x85\xb5g\xb6\xcc\xd4\x1a\xd3\x12E\x1b\x94\x8at\x13\xf0\xa1B\xfd@\xd4\x93G')

BLANK_ROOT_HASH = Hash32(b'V\xe8\x1f\x17\x1b\xccU\xa6\xff\x83E\xe6\x92\xc0\xf8n\x5bH\xe0\x1b\x99l\xad\xc0\x01b/\xb5\xe3c\xb4!')
