from datetime import date
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import requests

load_dotenv()

# Create a W3 Connection
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
st.write("This is the url",os.getenv("WEB3_PROVIDER_URI"))
# Set up Pinata Headers
json_headers = {
    "Content-Type":"application/json",
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY")
}

file_headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY")
}

def convert_data_to_json(content):
    data = {"pinataOptions":{"cidVersion":1}, 
            "pinataContent":content }
    return json.dumps(data)

def pin_file_to_ipfs(data):
    r = requests.post("https://api.pinata.cloud/pinning/pinFileToIPFS",
                      files={'file':data},
                      headers= file_headers)
    print(r.json())
    ipfs_hash = r.json()["IpfsHash"]
    return ipfs_hash

def pin_json_to_ipfs(json):
    r = requests.post("https://api.pinata.cloud/pinning/pinJSONToIPFS",
                      data=json,
                      headers= json_headers)
    print(r.json())
    ipfs_hash = r.json()["IpfsHash"]
    return ipfs_hash

def pin_nft(name, file,**kwargs):
    # Pin certificate picture to IPFS
    ipfs_file_hash = pin_file_to_ipfs(file.getvalue())

    # Build our NFT Token JSON
    token_json = {
       "name": name,
       "image": f"ipfs.io/ipfs/{ipfs_file_hash}"
    }

    # Add extra attributes if any passed in
    token_json.update(kwargs.items())

    # Add to pinata json to be uploaded to Pinata
    json_data = convert_data_to_json(token_json)

    # Pin the real NFT Token JSON
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash, token_json


######################################################################
## Load the contract
######################################################################

@st.cache(allow_output_mutation=True)
def load_contract():
    with open(Path("./contracts/compiled/Picture_abi.json")) as file:
        picture_abi = json.load(file)

    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    beach_contract = w3.eth.contract(address=contract_address,
                    abi=picture_abi)

    return beach_contract            

contract = load_contract()

account = st.text_input("Enter Account Address: ", value="0xC0277d02d43Ed6105029FE6c51Fa990E696147BC")

######################################################################
## Streamlit Inputs
######################################################################
st.markdown("## Create the NFT")

name = st.text_input("Enter the name of the Image: ")
artist = st.text_input("Enter the artist name")
image_details = st.text_input("Enter image Details: ")

# Upload the Certificate Picture File
file = st.file_uploader("Upload Image", type=["png","jpeg", "jpg"])


######################################################################
## Button to Award the Certificate
######################################################################

if st.button("Award NFT"):

    nft_ipfs_hash,token_json = pin_nft(name,file,  
             image_details=image_details)

    nft_uri = f"ipfs.io/ipfs/{nft_ipfs_hash}"
    st.write(nft_uri)
    # THIS ONLY WORKS IN GANACHE
    tx_hash = contract.functions.registerPicture(account, name, artist, image_details, nft_uri).transact({'from':account,'gas':1000000})
    # This generally works on the mainnet - Rinkeby, not so much
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)      

 
    st.write("Transaction mined")
    st.write(dict(receipt))

    st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    st.markdown(f"[NFT IPFS Gateway Link] (https://{nft_uri})")
    st.markdown(f"[NFT IPFS Image Link] (https://{token_json['image']})")