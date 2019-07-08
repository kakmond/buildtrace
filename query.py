from web3 import Web3
import json

# set ganache address
ganache_url = "http://127.0.0.1:8545"
# set path of json file (ABI)
contract_ABI = '/build/contracts/TraceStorage.json'
# set deployed address of the contract
contractAddress = '0xdb1BAc82401d673fe5EABF26F680fECAF2b9A16e' 

# set up web3 connection with Ganache
web3 = Web3(Web3.HTTPProvider(ganache_url))
with open(contract_ABI) as f:
    info_json = json.load(f)
abi = info_json["abi"]
bytecode = info_json['bytecode']
# create the contract instance with the deployed address
contract = web3.eth.contract(
address = web3.toChecksumAddress(contractAddress),
abi = abi,
)
# set account as sender
web3.eth.defaultAccount = web3.eth.accounts[0]
# display the trace data
print('Updated trace data: {}'.format(
    contract.functions.getTrace().call()
))