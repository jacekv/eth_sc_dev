import sys
sys.path.append("..")
from eth import utils

contract_address = utils.calcContractAddress("004ec07d2329997267ec62b4166639513386f32e", 0x8e)
assert contract_address == "8d7bb25141ff9c4c77e9e208b6bf4d1d3ca684b0", "Contract address differs"

print("Checks passed")
