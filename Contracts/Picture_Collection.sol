// SPDX License-Identifier
pragma solidity ^0.6.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v3.0.0/contracts/token/ERC721/ERC721.sol";

contract ImageCollection is ERC721 {
    constructor() public ERC721("ImageCollectionToken", "PIC") {}

    struct Picture {
        string name;
        string artist;
        uint256 date;
        string createdBy_address;

    }

    mapping(uint256 => Picture) public ImageCollection;

   
   function registerPicture(
        address owner,
        string memory name,
        string memory artist,
        string memory image_details,
        string memory tokenUri
        
    ) public returns (uint256) {
        uint256 tokenId = totalSupply();

        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenUri);

        ImageCollection[tokenId] = Picture(name, artist, now, "0xC0277d02d43Ed6105029FE6c51Fa990E696147BC");

        return tokenId;
    }

    
        
    
}
