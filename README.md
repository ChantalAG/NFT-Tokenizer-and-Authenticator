# NFT-Tokenizer-and-Authenticator
This project will mint NFTs for the end user and validate the authenticity of a given NFT. 


The NFT will store the account address used to sign the transaction as an attribute of the NFT.
The other details that will be stored in the NFT will be 1) Name 2) creation_time 3) description 4) creator_account_address 5) NFT_encrypted_data

the app will get a token from a trusted entity where the metamask account will be registered. The registration process will be a one time setup that will happen before the minting process.

This trusted entity will provide a one time token for the account address and keep a track of token issued i.e it will keep a mapping of account adress, time of token issuance and actual token

this token will then be used by the minting process to encrypt the 4 attributes of the NFT i.e 1) Name 2) creation_time 3) description 4) creator_account_address
the encrypted data will then be added to the NFT attributes and will be stored on the blockchain once th NFT is minted.

### Authentication
Anyone could create a similar NFT by copying the  attributes of the original NFT i.e 1) Name 2) creation_time 3) description  5) NFT_encrypted_data and only chnage the account address and pretend to be the original creator of the NFT
However, it will not have the token that was used to encrypt/decrypt the data. This token information will only be available with the trusted third party and the original creator of the NFT.
So in order to authenticate the NFT, the details of the NFT will be sent to the third party/or the original creator of the NFT if the creator offers a mechanism to authenticate the NFT.
The third party can decrypt the data using the token it generated for the account address and time, in this case it will not have the new account address or it will be mapped to a different token and thus the decryption will not be successful and the fraud can be identified.

Case 2
A fraud user could specify the same creator_account_address but change some other attribute of the NFT like Name or description. In that case, the third party will be able to decrypt the data as it will be able to find the token for the account address. However, after decryption, it will find that the decrypted data has a different Name than the name of the replicated NFT and thus can identify that the NFT is not original.
The original attributes of the NFT will have to match the decrypted data in order to confirm that the NFT is original

### MetamaskWebApp

### Set up instructions
1) python3 -m venv env
2) source env/bin/activate
3) pip3 install flask
4) set FLASK_APP=app.py
5) flask run
6) Running on http://127.0.0.1:5000/ 