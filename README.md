# mint-nft-python

## Get Started

This repository is minting NFT using python. Dependency Libraries are openzeppelin(Solidity), Web3.py and py-solc-x. So you have to install the libraries via npm and pip. If you finished preparing, you can mint the NFT.

```
$ npm install --prefix=./ @openzeppelin/contracts
$ pip install -r requirements.txt
$ python mint_nft.py
```

## Premise

- This repository is for Polygon Network.
  - (Probably works on Ethereum Network too!)
- You have to confirm the solc version on your enviroment. If your solc version is not `0.8.10`, please modify the version code of solc in the `mint_nft.py`.  
- In the case of changing the contract name, please modify the contract name and symbol name in the `solidity/MyNFT.sol`

## Preparing

If you want to mint the NFT using Polygon, you get the below enviroment. And you have to fill parameters in the nft_config.yaml.

- Infura URL
  - Ref: https://infura.io/
  - you have to signup and get the (Polygon) url.
- Your Address (on Polygon)
  - Ref: https://docs.polygon.technology/docs/develop/metamask/config-polygon-on-metamask/
  - Please write your public address on Polygon.
- Secret Key
  - Please copy from Metamask.
- Contract Address (on Polygon)
  - If this field is left blank, it will be created automatically in the `mint_nft.py`.
- Token URI(Metadata URI)
  - Ref: https://docs.openzeppelin.com/contracts/2.x/erc721
  - Please preapare the Token URI in advance.

## Documentation

- web3.py
  - https://web3py.readthedocs.io/en/stable/
- py-solc-x
  - https://pypi.org/project/py-solc-x/
- openzeppelin
  - https://openzeppelin.com/