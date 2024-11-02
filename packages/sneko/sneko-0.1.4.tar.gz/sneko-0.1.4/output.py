ABI='[{"inputs": [{"internalType": "uint256", "name": "_number", "type": "uint256"}], "stateMutability": "nonpayable", "type": "constructor"}, {"inputs": [], "name": "getNumber", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "number", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_number", "type": "uint256"}], "name": "setNumber", "outputs": [], "stateMutability": "nonpayable", "type": "function"}]'
BYTECODE="6080604052348015600e575f80fd5b5060405161020f38038061020f8339818101604052810190602e9190606b565b805f81905550506091565b5f80fd5b5f819050919050565b604d81603d565b81146056575f80fd5b50565b5f815190506065816046565b92915050565b5f60208284031215607d57607c6039565b5b5f6088848285016059565b91505092915050565b6101718061009e5f395ff3fe608060405234801561000f575f80fd5b506004361061003f575f3560e01c80633fb5c1cb146100435780638381f58a1461005f578063f2c9ecd81461007d575b5f80fd5b61005d600480360381019061005891906100e8565b61009b565b005b6100676100a4565b6040516100749190610122565b60405180910390f35b6100856100a9565b6040516100929190610122565b60405180910390f35b805f8190555050565b5f5481565b5f8054905090565b5f80fd5b5f819050919050565b6100c7816100b5565b81146100d1575f80fd5b50565b5f813590506100e2816100be565b92915050565b5f602082840312156100fd576100fc6100b1565b5b5f61010a848285016100d4565b91505092915050565b61011c816100b5565b82525050565b5f6020820190506101355f830184610113565b9291505056fea264697066735822122036cb1d6334398b2a35588a0ddd316ea19a8afa4602f88c7c3b0cb1df0e2f837a64736f6c634300081a0033"

from web3 import Web3, EthereumTesterProvider


w3 = Web3(EthereumTesterProvider())
contract_factory = w3.eth.contract(abi=ABI, bytecode=BYTECODE)

# provide `constructor` args if necessary:
tx_hash = contract_factory.constructor(123).transact()
contract_address = w3.eth.get_transaction_receipt(tx_hash)["contractAddress"]
contract = w3.eth.contract(address=contract_address, abi=ABI)

# set a breakpoint to inspect the contract object:
import pdb; pdb.set_trace()  # noqa

# result = contract.functions.exampleFunction().call()
