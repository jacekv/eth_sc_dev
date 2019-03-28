from structures.blockHeader import Blockheader
from eth_typing import Address
from constants import ZERO_ADDRESS


class ExecutionEnvironment(object):
    """
    Tries to implement the execution environment as defined in the yellow paper
    under 9.3. It contains the following values:

    - Ia (addressOwningCode): the address of the account which owns the code that is executing.
    - Io (senderAddress): the sender address of the transaction that originated this execution.
    - Ip (gasPrice): the price of gas in the transaction that originated this execution.
    - Id (inputData): the byte array that is the input data to this execution;
      if the execution agent is a transaction, this would be the transaction data.
    - Is (addressCausingExec): the address of the account which caused the code to be executing;
      if the execution agent is a transaction, this would be the transaction sender.
      (it's the message sender. It changes with every call and create.)
    - Iv (value): the value, in Wei, passed to this account as part of the same
      procedure as execution; if the execution agent is a transaction, this
      would be the transaction value.
    - Ib (code): the byte array that is the machine code to be executed.
    - IH (blockheader): the block header of the present block.
    - Ie (depthMsgCall): the depth of the present message-call or contract-creation
      (i.e. the number of CALLs or CREATEs being executed at present).
    - Iw (permissionStateMod): the permission to make modifications to the state.
    """

    def __init__(self,
                 code: str,
                 depthMsgCall: int = 0,
                 value: int = 0,
                 gasPrice: int = 0,
                 inputData: str = '0',
                 senderAddress: Address = ZERO_ADDRESS,
                 addressOwningCode: Address = ZERO_ADDRESS,
                 addressCausingExec: Address = ZERO_ADDRESS,
                 blockHeader: Blockheader = None,
                 permissionStateMod=None) -> None:
        self.machineCode = code
        self.depthMsgCall = depthMsgCall
        self.blockHeader = blockHeader
        self.value = value
        self.gasPrice = gasPrice
        self.inputData = inputData
        self.senderAddress = senderAddress
        self.addressOwningCode = addressOwningCode
        self.addressCausingExec = addressCausingExec
        self.permissionStateMod = permissionStateMod
