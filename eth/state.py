class State(object):

    def __init__(self):
        self.storage = {}

    def get_nonce(self, address: str) -> int:
        if address in self.storage:
            return self.storage[address]['nonce']
        return 0

    def get_balance(self, address) -> int:
        if address in self.storage:
            return self.storage[address]['balance']
        return 0

    def get_storageRoot(self, address) -> int:
        if address in self.storage:
            return self.storage[address]['storageRoot']
        return 0

    def get_codeHash(self, address) -> int:
        if address in self.storage:
            return self.storage[address]['codeHash']
        return 0



if __name__ == "__main__":
    w = WorldState()
    print(w.nonce("ad"))