import sys
import os
import pprint
import inspect
import yaml
import base64
from xml.dom import minidom
import mimetypes

from web3 import Web3, IPCProvider
from web3.providers.rpc import HTTPProvider
from web3.middleware import geth_poa_middleware
from solcx import compile_source

def parse_svg_file(file, encode=False):
  if mimetypes.guess_type(file)[0] != 'image/svg+xml':
    return False
  doc = minidom.parse(file)
  res = doc.toprettyxml() if encode == False else base64.b64encode(doc.toprettyxml().encode('utf-8'))
  return res

def get_checksum_address(w3, address):
  if(w3.isChecksumAddress(address) == False):
    address = w3.toChecksumAddress(address)
  return address

def compile_source_file(file_path, solc_version, base_path):
  with open(file_path, 'r') as f:
    source = f.read()
  compiled_sol = compile_source(source,
    output_values=['abi', 'bin'],
    solc_version=solc_version,
    base_path=base_path
  )    
  return compiled_sol

def deploy_contract(w3, contract_interface, private_key):
  user_address = from_address = w3.eth.defaultAccount
  contract = get_contract(w3, contract_interface)
  base_txn = get_base_txn(w3, user_address, from_address) 
  contract_txn = contract.constructor().buildTransaction(base_txn)

  signed_txn = get_sign_txn(w3, contract_txn, private_key)
  receipt = send_txn(w3, signed_txn)
  return receipt['contractAddress']
  
def get_contract(w3, contract_interface, contract_address = None):
  if contract_address is not None:
    contract_address = get_checksum_address(w3, contract_address)
    contract = w3.eth.contract(
      address=contract_address,
      abi=contract_interface['abi'],
      bytecode=contract_interface['bin']
    )
  else:
    contract = w3.eth.contract(
      abi=contract_interface['abi'],
      bytecode=contract_interface['bin']
    )
  return contract
 
def get_nonce(w3, address):
  address = get_checksum_address(w3, address)
  return w3.eth.get_transaction_count(address)

def get_sign_mint_txn(w3, contract, user_address, private_key, image_xml):  
  user_address = get_checksum_address(w3, user_address)
  base_txn = get_base_txn(w3, user_address)
  mint_txn = contract.functions.mintNFT(image_xml, '... input name ...', '... input description ..').buildTransaction(base_txn)
  pprint.pprint(mint_txn);
  sign_mint_txn = get_sign_txn(w3, mint_txn, private_key)
  return sign_mint_txn

def get_sign_txn(w3, tx, private_key):
  return w3.eth.account.sign_transaction(tx, private_key=private_key)

def get_base_txn(w3, user_address, from_address=None):
  user_address = get_checksum_address(w3, user_address)
  base_txn = {
    'nonce': get_nonce(w3, user_address),
    'gas': 10000000,
    'gasPrice': w3.toWei('1.2', 'gwei')
  }  
  if from_address is not None:
    from_address = get_checksum_address(w3, from_address)
    base_txn['from'] = from_address
  return base_txn

def send_txn(w3, signed_txn):
  w3.eth.send_raw_transaction(signed_txn.rawTransaction)
  txn_hash = w3.toHex(w3.keccak(signed_txn.rawTransaction))
  print(f"txn hash: {txn_hash} ")
  return w3.eth.wait_for_transaction_receipt(txn_hash)

if __name__ == '__main__':
  
  try:
    # read yaml file
    with open('nft_config.yaml', 'r') as yml:
      config = yaml.safe_load(yml)
    if os.environ.get('ENV') is None:
      env = 'dev'
    
    # read svg
    file = sys.argv[1]
    image_xml = parse_svg_file(file)
    if image_xml == False:
      raise Exception('Input file is not svg')

    # load config value
    user_address = config[env]['user_address']
    private_key = config[env]['private_key']
    contract_address = config[env]['contract_address']
    
    # w3 instance
    polygon_infura_url = config[env]['infura_url']
    w3 = Web3(Web3.HTTPProvider(polygon_infura_url))
    
    # set default address
    w3.eth.defaultAccount = w3.toChecksumAddress(user_address)
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    print(f"BlockChain conection is = {w3.isConnected()}") 

    # build contract
    compiled_sol = compile_source_file('solidity/MyNFT_OnChain.sol', '0.8.11', 'node_modules')
    contract_id = next(iter(compiled_sol))
    contract_interface = compiled_sol[contract_id]
    
    # deploy contract
    if contract_address == '' or contract_address is None:
      contract_address = deploy_contract(w3, contract_interface, private_key)
      print(f'Deployed {contract_id} to: {contract_address}\n')
    
    # get contract
    contract = get_contract(w3, contract_interface, contract_address)
    
    # build txn
    sign_mint_txn = get_sign_mint_txn(w3, contract, user_address, private_key, image_xml)
    pprint.pprint(f"sign_mint_txn : {sign_mint_txn}")
    
    # send txn
    receipt = send_txn(w3, sign_mint_txn)
    hex_tokenid = receipt["logs"][0]["topics"][3].hex()
    tokenid = int(hex_tokenid, 16) 
    print(f"Got contract tokenid: {tokenid}")
    
  except Exception as e:
    tb = sys.exc_info()[2]
    print("message:{0}".format(e.with_traceback(tb)))
    print('Can not finish the process')