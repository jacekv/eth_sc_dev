#Solidity OPODES

## Table
Table taken from: https://raw.githubusercontent.com/trailofbits/evm-opcodes/master/README.md

In the description of each instruction I might be using Stack[X] where X is a
uint. Stack[0] is the latest pushed value, Stack[1] is right below. Stack[0]
means that the value is popped from the stack and using during the operation.
Stack[0] = Stack[0] + Stack[1] means that the values from Stack[0] and Stack[1]
are poped, added and the result is pushed back on the stack.

| Opcode | Name | Description | Extra Info | Gas | Implemented | Description |
| --- | --- | --- | --- | --- | --- | --- |
| `0x00` | STOP | Halts execution | - | 0 | | |
| `0x01` | ADD | Addition operation | - | 3 | X | Stack[0] = Stack[0] + Stack[1] |
| `0x02` | MUL | Multiplication operation | - | 5 | X | Stack[0] = Stack[0] * Stack[1] |
| `0x03` | SUB | Subtraction operation | - | 3 | X | Stack[0] = Stack[0] - Stack[1] |
| `0x04` | DIV | Integer division operation | - | 5 | X | Stack[0] = Stack[0] / Stack[1] |
| `0x05` | SDIV | Signed integer division operation (truncated) | - | 5 | X | Stack[0] = Stack[0] / Stack[1] |
| `0x06` | MOD | Modulo remainder operation | - | 5 | X | Stack[0] = Stack[0] % Stack[1] |
| `0x07` | SMOD | Signed modulo remainder operation | - | 5 | X | Stack[0] = Stack[0] % Stack[1] |
| `0x08` | ADDMOD | Modulo addition operation | - | 8 | X | Stack[0] = (Stack[0] + Stack[1]) mod Stack[2] |
| `0x09` | MULMOD | Modulo multiplication operation | - | 8 | X | Stack[0] = (Stack[0] * Stack[1]) mod Stack[2] |
| `0x0a` | EXP | Exponential operation | - | 10* | X | Stack[0] = Stack[0] ** Stack[1] |
| `0x0b` | SIGNEXTEND | Extend length of two's complement signed integer | - | 5 | X | |
| `0x0c` - `0x0f` | Unused | Unused | - | - | - | - |
| `0x10` | LT | Less-than comparison | - | 3 | X | Stack[0] = Stack[0] < Stack[1] |
| `0x11` | GT | Greater-than comparison | - | 3 | X | Stack[0] = Stack[0] > Stack[1] |
| `0x12` | SLT | Signed less-than comparison | - | 3 | X | Stack[0] = Stack[0] < Stack[1] |
| `0x13` | SGT | Signed greater-than comparison | - | 3 | X | Stack[0] = Stack[0] > Stack[1] |
| `0x14` | EQ | Equality comparison | - | 3 | X | Stack[0] = Stack[0] == Stack[1] |
| `0x15` | ISZERO | Simple not operator | - | 3 | X | Stack[0] = 1 if Stack[0] == 0, else 0 |
| `0x16` | AND | Bitwise AND operation | - | 3 | X | Stack[0] = Stack[0] AND STACK[1] |
| `0x17` | OR | Bitwise OR operation | - | 3 | X | Stack[0] = Stack[0] OR STACK[1] |
| `0x18` | XOR | Bitwise XOR operation | - | 3 | X | Stack[0] = Stack[0] XOR STACK[1] |
| `0x19` | NOT | Bitwise NOT operation | - | 3 | X | Stack[0] = NOT Stack[0] |
| `0x1a` | BYTE | Retrieve single byte from word | - | 3 | X | |
| `0x20` | SHA3 | Compute Keccak-256 hash | - | 30* | | |
| `0x21` - `0x2f`| Unused | Unused | - | - | - | - |
| `0x30` | ADDRESS | Get address of currently executing account and push on the stack| Check `execution environment` in YP for `I_a`| 2 | X | Stack[0] = `I_a`|
| `0x31` | BALANCE | Get balance of the given account | Stack[0] has an address | 400 | | Stack[0] = State[Stack[0]]_b |
| `0x32` | ORIGIN | Get execution origination address and push on the stack | Check `execution environment` in YP for `I_o` | 2 | X | Stack[0] = `I_o`|
| `0x33` | CALLER | Get caller address and push on the stack | Check `execution environment` in YP for `I_s` | 2 | X | Stack[0] = `I_s`|
| `0x34` | CALLVALUE | Get deposited value by the instruction/transaction responsible for this execution and push on the stack | Check `execution environment` in YP for `I_v` | 2 | X | Stack[0] = `I_v` |
| `0x35` | CALLDATALOAD | Get input data of current environment | Check `execution environment` in YP for `I_d` | 3 | X | Stack[0] = `I_d`[Stack[0]...(Stack[0] + 31)]|
| `0x36` | CALLDATASIZE | Get size of input data in current environment | Check `execution environment` in YP for `I_d` | 2* | X | Stack[0] = len(`I_d`)|
| `0x37` | CALLDATACOPY | Copy input data in current environment to memory | - | 3 | | |
| `0x38` | CODESIZE | Get size of code running in current environment | Check `execution environment` in YP for `I_b` | 2 | X | Stack[0] = len(`I_b`)|
| `0x39` | CODECOPY | Copy code running in current environment to memory | - | 3* | | |
| `0x3a` | GASPRICE | Get price of gas in current environment | Check `execution environment` in YP for `I_b` | 2 | X | Stack[0] = `I_p` |
| `0x3b` | EXTCODESIZE | Get size of an account's code | - | 700 | | |
| `0x3c` | EXTCODECOPY | Copy an account's code to memory | - | 700* | | |
| `0x3d` | RETURNDATASIZE | Pushes the size of the return data buffer onto the stack |  [EIP 211](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-211.md) | 2 | | |
| `0x3e` | RETURNDATACOPY | Copies data from the return data buffer to memory | [EIP 211](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-211.md) | 3 | | |
| `0x3f` | Unused | - | - | - | - | - |
| `0x40` | BLOCKHASH | Get the hash of one of the 256 most recent complete blocks | - | 20 | | |
| `0x41` | COINBASE | Get the block's beneficiary address | - | 2 | X | Stack[0] = Blockheader.Coinbase |
| `0x42` | TIMESTAMP | Get the block's timestamp | - | 2 | X | Stack[0] = Blockheader.Timestamp |
| `0x43` | NUMBER | Get the block's number | - | 2 | X | Stack[0] = Blockheader.BlockNumber |
| `0x44` | DIFFICULTY | Get the block's difficulty | - | 2 | X | Stack[0] = Blockheader.Difficulty |
| `0x45` | GASLIMIT | Get the block's gas limit | - | 2 | X | Stack[0] = Blockheader.GasLimit |
| `0x46` - `0x4f` | Unused | - | - | - | - | - |
| `0x50` | POP | Remove word from stack | - | 2 | X | Remove top most item from stack |
| `0x51` | MLOAD | Load word from memory | - | 3* | | |
| `0x52` | MSTORE | Save word to memory | - | 3* | | |
| `0x53` | MSTORE8 | Save byte to memory | - | 3 | | |
| `0x54` | SLOAD | Load word from storage | - | 200 | | |
| `0x55` | SSTORE | Save word to storage | - | 20000** | | |
| `0x56` | JUMP | Alter the program counter | - | 8 | X | PC = Stack[0] |
| `0x57` | JUMPI | Conditionally alter the program counter | - | 10 | X | Set PC = Stack[0] if Stack[1] != 0, else PC += 1|
| `0x58` | GETPC | Get the value of the program counter prior to the increment | - | 2 | X | Stack[0] = PC|
| `0x59` | MSIZE | Get the size of active memory in bytes | - | 2 | | |
| `0x5a` | GAS | Get the amount of available gas, including the corresponding reduction the amount of available gas | - | 2 | | |
| `0x5b` | JUMPDEST | Mark a valid destination for jumps. No effect on machine state | - | 1 | X | - |
| `0x5c` - `0x5f` | Unused | - | - | - | - | - |
| `0x60` | PUSH1 | Place 1 byte item on stack | - | 3 | X | Push 1 byte on stack |
| `0x61` | PUSH2 | Place 2-byte item on stack | - | 3 | X | Push 2 byte on stack |
| `0x62` | PUSH3 | Place 3-byte item on stack | - | 3 | X | Push 3 byte on stack |
| `0x63` | PUSH4 | Place 4-byte item on stack | - | 3 | X | Push 4 byte on stack |
| `0x64` | PUSH5 | Place 5-byte item on stack | - | 3 | X | Push 5 byte on stack |
| `0x65` | PUSH6 | Place 6-byte item on stack | - | 3 | X | Push 6 byte on stack |
| `0x66` | PUSH7 | Place 7-byte item on stack | - | 3 | X | Push 7 byte on stack |
| `0x67` | PUSH8 | Place 8-byte item on stack | - | 3 | X | Push 8 byte on stack |
| `0x68` | PUSH9 | Place 9-byte item on stack | - | 3 | X | Push 9 byte on stack |
| `0x69` | PUSH10 | Place 10-byte item on stack | - | 3 | X | Push 10 byte on stack |
| `0x6a` | PUSH11 | Place 11-byte item on stack | - | 3 | X | Push 11 byte on stack |
| `0x6b` | PUSH12 | Place 12-byte item on stack | - | 3 | X | Push 12 byte on stack |
| `0x6c` | PUSH13 | Place 13-byte item on stack | - | 3 | X | Push 13 byte on stack |
| `0x6d` | PUSH14 | Place 14-byte item on stack | - | 3 | X | Push 14 byte on stack |
| `0x6e` | PUSH15 | Place 15-byte item on stack | - | 3 | X | Push 15 byte on stack |
| `0x6f` | PUSH16 | Place 16-byte item on stack | - | 3 | X | Push 16 byte on stack |
| `0x70` | PUSH17 | Place 17-byte item on stack | - | 3 | X | Push 17 byte on stack |
| `0x71` | PUSH18 | Place 18-byte item on stack | - | 3 | X | Push 18 byte on stack |
| `0x72` | PUSH19 | Place 19-byte item on stack | - | 3 | X | Push 19 byte on stack |
| `0x73` | PUSH20 | Place 20-byte item on stack | - | 3 | X | Push 20 byte on stack |
| `0x74` | PUSH21 | Place 21-byte item on stack | - | 3 | X | Push 21 byte on stack |
| `0x75` | PUSH22 | Place 22-byte item on stack | - | 3 | X | Push 22 byte on stack |
| `0x76` | PUSH23 | Place 23-byte item on stack | - | 3 | X | Push 23 byte on stack |
| `0x77` | PUSH24 | Place 24-byte item on stack | - | 3 | X | Push 24 byte on stack |
| `0x78` | PUSH25 | Place 25-byte item on stack | - | 3 | X | Push 25 byte on stack |
| `0x79` | PUSH26 | Place 26-byte item on stack | - | 3 | X | Push 26 byte on stack |
| `0x7a` | PUSH27 | Place 27-byte item on stack | - | 3 | X | Push 27 byte on stack |
| `0x7b` | PUSH28 | Place 28-byte item on stack | - | 3 | X | Push 28 byte on stack |
| `0x7c` | PUSH29 | Place 29-byte item on stack | - | 3 | X | Push 29 byte on stack |
| `0x7d` | PUSH30 | Place 30-byte item on stack | - | 3 | X | Push 30 byte on stack |
| `0x7e` | PUSH31 | Place 31-byte item on stack | - | 3 | X | Push 31 byte on stack |
| `0x7f` | PUSH32 | Place 32-byte (full word) item on stack | - |  3 |  X |  Push 32 byte on stack |
| `0x80` | DUP1 | Duplicate 1st stack item | - |  3 | X | Stack[0] = Stack[1] |
| `0x81` | DUP2 | Duplicate 2nd stack item | - | 3 | X | Stack[0] = Stack[2] |
| `0x82` | DUP3 | Duplicate 3rd stack item | - | 3 | X | Stack[0] = Stack[3] |
| `0x83` | DUP4 | Duplicate 4th stack item | - | 3 | X | Stack[0] = Stack[4] |
| `0x84` | DUP5 | Duplicate 5th stack item | - | 3 | X | Stack[0] = Stack[5] |
| `0x85` | DUP6 | Duplicate 6th stack item | - | 3 | X | Stack[0] = Stack[6] |
| `0x86` | DUP7 | Duplicate 7th stack item | - | 3 | X | Stack[0] = Stack[7] |
| `0x87` | DUP8 | Duplicate 8th stack item | - | 3 | X | Stack[0] = Stack[8] |
| `0x88` | DUP9 | Duplicate 9th stack item | - | 3 | X | Stack[0] = Stack[9] |
| `0x89` | DUP10 | Duplicate 10th stack item | - | 3 | X | Stack[0] = Stack[10] |
| `0x8a` | DUP11 | Duplicate 11th stack item | - | 3 | X | Stack[0] = Stack[11] |
| `0x8b` | DUP12 | Duplicate 12th stack item | - | 3 | X | Stack[0] = Stack[12] |
| `0x8c` | DUP13 | Duplicate 13th stack item | - | 3 | X | Stack[0] = Stack[13] |
| `0x8d` | DUP14 | Duplicate 14th stack item | - | 3 | X | Stack[0] = Stack[14] |
| `0x8e` | DUP15 | Duplicate 15th stack item | - | 3 | X | Stack[0] = Stack[15] |
| `0x8f` | DUP16 | Duplicate 16th stack item | - | 3 | X | Stack[0] = Stack[16] |
| `0x90` | SWAP1 | Exchange 1st and 2nd stack items | - | 3 | X | Stack[0] <=> Stack[1] |
| `0x91` | SWAP2 | Exchange 1st and 3rd stack items | - | 3 | X | Stack[0] <=> Stack[2] |
| `0x92` | SWAP3 | Exchange 1st and 4th stack items | - | 3 | X | Stack[0] <=> Stack[3] |
| `0x93` | SWAP4 | Exchange 1st and 5th stack items | - | 3 | X | Stack[0] <=> Stack[4] |
| `0x94` | SWAP5 | Exchange 1st and 6th stack items | - | 3 | X | Stack[0] <=> Stack[5] |
| `0x95` | SWAP6 | Exchange 1st and 7th stack items | - | 3 | X | Stack[0] <=> Stack[6] |
| `0x96` | SWAP7 | Exchange 1st and 8th stack items | - | 3 | X | Stack[0] <=> Stack[7] |
| `0x97` | SWAP8 | Exchange 1st and 9th stack items | - | 3 | X | Stack[0] <=> Stack[8] |
| `0x98` | SWAP9 | Exchange 1st and 10th stack items | - | 3 | X | Stack[0] <=> Stack[9] |
| `0x99` | SWAP10 | Exchange 1st and 11th stack items | - | 3 | X | Stack[0] <=> Stack[10] |
| `0x9a` | SWAP11 | Exchange 1st and 12th stack items | - | 3 | X | Stack[0] <=> Stack[11] |
| `0x9b` | SWAP12 | Exchange 1st and 13th stack items | - | 3 | X | Stack[0] <=> Stack[12] |
| `0x9c` | SWAP13 | Exchange 1st and 14th stack items | - | 3 | X | Stack[0] <=> Stack[13] |
| `0x9d` | SWAP14 | Exchange 1st and 15th stack items | - | 3 | X | Stack[0] <=> Stack[14] |
| `0x9e` | SWAP15 | Exchange 1st and 16th stack items | - | 3 | X | Stack[0] <=> Stack[15] |
| `0x9f` | SWAP16 | Exchange 1st and 17th stack items | - | 3 | X | Stack[0] <=> Stack[16] |
| `0xa0` | LOG0 | Append log record with no topics | - | 375 | | |
| `0xa1` | LOG1 | Append log record with one topic | - | 750 | | |
| `0xa2` | LOG2 | Append log record with two topics | - | 1125 | | |
| `0xa3` | LOG3 | Append log record with three topics | - | 1500 | | |
| `0xa4` | LOG4 | Append log record with four topics | - | 1875 | | |
| `0xa5` - `0xaf` | Unused | - | - | - | - | - |
| `0xb0` | JUMPTO | Tentative [libevmasm has different numbers](https://github.com/ethereum/solidity/blob/c61610302aa2bfa029715b534719d25fe3949059/libevmasm/Instruction.h#L176)| [EIP 615](https://github.com/ethereum/EIPs/blob/606405b5ab7aa28d8191958504e8aad4649666c9/EIPS/eip-615.md) | | | |
| `0xb1` | JUMPIF | Tentative | [EIP 615](https://github.com/ethereum/EIPs/blob/606405b5ab7aa28d8191958504e8aad4649666c9/EIPS/eip-615.md) | | | |
| `0xb2` | JUMPSUB | Tentative | [EIP 615](https://github.com/ethereum/EIPs/blob/606405b5ab7aa28d8191958504e8aad4649666c9/EIPS/eip-615.md) | | | |
| `0xb4` | JUMPSUBV | Tentative | [EIP 615](https://github.com/ethereum/EIPs/blob/606405b5ab7aa28d8191958504e8aad4649666c9/EIPS/eip-615.md) | | | |
| `0xb5` | BEGINSUB | Tentative | [EIP 615](https://github.com/ethereum/EIPs/blob/606405b5ab7aa28d8191958504e8aad4649666c9/EIPS/eip-615.md) | | | |
| `0xb6` | BEGINDATA | Tentative | [EIP 615](https://github.com/ethereum/EIPs/blob/606405b5ab7aa28d8191958504e8aad4649666c9/EIPS/eip-615.md) | | | |
| `0xb8` | RETURNSUB | Tentative | [EIP 615](https://github.com/ethereum/EIPs/blob/606405b5ab7aa28d8191958504e8aad4649666c9/EIPS/eip-615.md) | | | |
| `0xb9` | PUTLOCAL | Tentative | [EIP 615](https://github.com/ethereum/EIPs/blob/606405b5ab7aa28d8191958504e8aad4649666c9/EIPS/eip-615.md) | | | |
| `0xba` | GETLOCAL | Tentative | [EIP 615](https://github.com/ethereum/EIPs/blob/606405b5ab7aa28d8191958504e8aad4649666c9/EIPS/eip-615.md) | | | |
| `0xbb` - `0xe0` | Unused | - | - | - | - | - |
| `0xe1` | SLOADBYTES | Only referenced in pyethereum | - | - | | |
| `0xe2` | SSTOREBYTES | Only referenced in pyethereum | - | - | | |
| `0xe3` | SSIZE | Only referenced in pyethereum | - | - | | |
| `0xe4` - `0xef` | Unused | - | - | - | - | - |
| `0xf0` | CREATE | Create a new account with associated code | - | - | 32000 | |
| `0xf1` | CALL | Message-call into an account | - | Complicated | | |
| `0xf2` | CALLCODE | Message-call into this account with alternative account's code | - | Complicated | | |
| `0xf3` | RETURN | Halt execution returning output data | - | 0 | | |
| `0xf4` | DELEGATECALL | Message-call into this account with an alternative account's code, but persisting into this account with an alternative account's code| - | - | Complicated | |
| `0xf5` | CALLBLACKBOX | - | - | | 40 | |
| `0xf6` - `0xf9` | Unused | - | - | - | - | - |
| `0xfa` | STATICCALL | Similar to CALL, but does not modify state | - | 40 | | |
| `0xfb` | CREATE2 | Create a new account and set creation address to `sha3(sender + sha3(init code)) % 2**1 |60` | - | | |
| `0xfc` | TXEXECGAS | Not in yellow paper FIXME | - | - | | |
| `0xfd` | REVERT | Stop execution and revert state changes, without consuming all provided gas and providing a reason | | - | 0 | |
| `0xfe` | INVALID | Designated invalid instruction | - | 0 | | |
| `0xff` | SELFDESTRUCT | Halt execution and register account for later deletion | - | 5000* | | | |
