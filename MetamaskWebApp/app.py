# ------------------------------------------------------------------------------
# Imports
from flask import Flask, render_template
from datetime import date
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import requests

# ------------------------------------------------------------------------------
# Flask App

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mint_nft', methods=['POST'])
def mint_nft():
    pic = request.files["pic"]
    if not pic:
        return 'No pic uploaded', 400
    file_name = secure_filename(pic.filename)
    mimetype = pic.mimetype

    # return render_template('index.html')
    return 'Image has been uploaded', 200




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

def load_contract():
    with open(Path("./contracts/compiled/Picture_abi.json")) as file:
        picture_abi = json.load(file)

    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    beach_contract = w3.eth.contract(address=contract_address,
                    abi=picture_abi)

    return beach_contract    





def generate_nft():

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

    contract = load_contract()

    nft_ipfs_hash,token_json = pin_nft(name,file,  
             image_details=image_details)

    nft_uri = f"ipfs.io/ipfs/{nft_ipfs_hash}"
    st.write(nft_uri)
    # THIS ONLY WORKS IN GANACHE
    tx_hash = contract.functions.registerPicture(account, name, artist, image_details, nft_uri).transact({'from':account,'gas':1000000})
    # This generally works on the mainnet - Rinkeby, not so much
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)      

    complete_uril = "https://{nft_uri})"
    complete_ipfs_gateway_link = "https://{token_json['image']}"