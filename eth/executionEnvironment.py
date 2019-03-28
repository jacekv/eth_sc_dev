
class ExecutionEnvironment(object):
    """
    Tries to implement the execution environment as defined in the yellow paper
    under 9.3. It contains the following values:

    - Ia: the address of the account which owns the code that is executing.
    - Io: the sender address of the transaction that originated this execution.
    - Ip: the price of gas in the transaction that originated this execution.
    - Id: the byte array that is the input data to this execution;
      if the execution agent is a transaction, this would be the transaction data.
    - Is: the address of the account which caused the code to be executing;
      if the execution agent is a transaction, this would be the transaction sender.
      (it's the message sender. It changes with every call and create.)
    - Iv: the value, in Wei, passed to this account as part of the same
      procedure as execution; if the execution agent is a transaction, this
      would be the transaction value.
    - Ib: the byte array that is the machine code to be executed.
    - IH: the block header of the present block.
    - Ie: the depth of the present message-call or contract-creation
      (i.e. the number of CALLs or CREATEs being executed at present).
    - Iw: the permission to make modifications to the state.
    """
    accountAddressOwningCode = None
    senderAddress = None
    gasPrice = None
    inputData = None
    accountAddressCausingExec = None
    value = None
    machineCode = None
    blockHeader = None
    depthMsgCall = None
    permissionStateMod = None

    def __init__(self, code):
        self.machineCode = code
