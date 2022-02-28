// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/utils/Base64.sol";

contract MyNFT is ERC721, Ownable{

	using Counters for Counters.Counter;
  Counters.Counter private _tokenIds;
  string private _img = '';
  string private _name = '';
  string private _description = '';

  constructor() public ERC721(
    'My NFT mint', 
    'My NFT'
  ) {}

  function mintNFT(string memory img, string memory name, string memory description) public onlyOwner returns (uint256) {
    _img = img;
    _name = name;
    _description = description;
    _tokenIds.increment();
    uint256 newItemId = _tokenIds.current();
    _safeMint(_msgSender(), newItemId);
    return newItemId;
  }

	function tokenURI(uint256 tokenId) public view override returns (string memory) {
		require(_exists(tokenId), "ERC721Metadata: URI query for nonexistent token");
		string memory img = _getImageString();
    string memory name = _getNameString();
    string memory description = _getDescString();
		bytes memory json = abi.encodePacked(
			'{"name": "My NFT #',
      Strings.toString(tokenId),
      '. ',
      name,
      '", "description": "My NFT. ',
      description,
      '", "image": "data:image/svg+xml;base64,',
			Base64.encode(bytes(img)),
			'"}'
		);
		return string(abi.encodePacked("data:application/json;base64,", Base64.encode(json)));
	}

  function _getImageString() private view returns (string memory) {
		return string(abi.encodePacked(_img));
	}

  function _getNameString() private view returns (string memory) {
		return string(_name);
	}

  function _getDescString() private view returns (string memory) {
		return string(_description);
	}

}